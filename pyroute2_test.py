#!/bin/env python
import pyroute2
#from pyroute2 import IPRoute
import time
import sys
import os
import pprint
import warnings



'''
RTM_DELADDR
'''

def check_ipv4_addr_add(x,index):
    print 'hello1'
    return x.get('index', None) == index \
        and x.get('event', None) =='RTM_NEWADDR' \
        and x.get('family') == 2
def check_ipv4_addr_del(x,index):
    print 'hello2'
    return x.get('index', None) == index \
        and x.get('event', None) =='RTM_DELADDR'\
        and x.get('family') == 2



def reg_new_route_ipv4(x,index):
    print 'hello3'

    return x.get('event', None)=='RTM_NEWROUTE' \
        and  x.get('family', None)==2
def reg_new_route_ipv6(x,index):
    print 'hello4'

    return x.get('event', None)=='RTM_NEWROUTE' \
        and  x.get('family', None)==10

def reg_event_all(x,index):
    print 'hello5'
    return True


def check_link_up(x,index):

    print 'hello6'
    return x.get('event', None)=='RTM_NEWLINK' \
        and  x.get('family', None)==0 \
        and x.get('index', None)==index\
        and x.get('__align', None)== 0 \
        and x.get('attrs', None)[2][1]== 'UP'
        
def check_link_down(x,index):
    return x.get('event', None)=='RTM_NEWLINK' \
        and  x.get('family', None)==0 \
        and x.get('index', None)==index\
        and x.get('__align', None)== 0 \
        and x.get('attrs', None)[2][1]== 'DOWN'

    
def nl_evnet_newlink_up(msg):
    print '%s--> %s'%(sys._getframe().f_code.co_name,msg)
def nl_evnet_newlink_down(msg):
    print '%s--> %s'%(sys._getframe().f_code.co_name,msg)
def nl_evnet_newroute_add(msg):
    print '%s--> %s'%(sys._getframe().f_code.co_name,msg)
def nl_evnet_newroute_del(msg):
    print '%s--> %s'%(sys._getframe().f_code.co_name,msg)
def nl_evnet_newaddr_add(msg):
    print '%s--> %s'%(sys._getframe().f_code.co_name,msg)
def nl_evnet_newaddr_del(msg):
    print '%s--> %s'%(sys._getframe().f_code.co_name,msg)
def nl_evnet_all(msg):
    print '%s--> %s'%(sys._getframe().f_code.co_name,msg)
    

class pyroute_test():
    def __init__(self):
        self.BRIDGE_IFNAME = 'br0'
        self.GE_IFNAME = 'p32p1'
        self.WIFI_IFNAME = 'ra0'
        self.nl = pyroute2.IPRoute()
        self.ifaces = pyroute2.IPDB(nl = self.nl, mode = 'direct')
        pass

        
    def create_bridge(self):
        print "add bridge"
        self.nl = pyroute2.IPRoute()
        self.ifaces = pyroute2.IPDB(nl = self.nl, mode = 'direct')
        bridge = self.ifaces.create(kind = 'bridge', ifname = self.BRIDGE_IFNAME)
        bridge.up()
        for ifname in ['ra0','p32p1']:
            iface = self.ifaces.get(ifname)
            iface.up()
            bridge.add_port(iface)
        pass
    def delete_bridge(self):
        print "delete bridge"
        bridge = self.ifaces.get(self.BRIDGE_IFNAME)
        ge = self.ifaces.get(self.GE_IFNAME)
        wifi = self.ifaces.get(self.WIFI_IFNAME)
        if bridge is not None:
            if ge is not None:
                bridge.del_port(ge)
            if wifi is not None:
                bridge.del_port(wifi)
            bridge.down()
            bridge.remove()
        self.ifaces.release()
        self.nl.release()
    def show(self):
        print os.popen("ip link |grep state |awk '{print $2}'").read()
    def test(self):
        while True:
            self.create_bridge()
            self.show()
            time.sleep(3)
            self.delete_bridge()
            self.show()
            time.sleep(3)
    def update_index(self):
        all = self.ifaces
        result = []
        for item in all :
            result.append(item)
        self.keytable={}
        lenght = len(result)/2
        for i in range(0,lenght):            
            key = result[i+lenght]
            value = result[i]
            self.keytable[key] = value-1
        print self.keytable
    def get_index_from_iface(self,iface):
        
        if self.keytable.has_key(iface) :
            return self.keytable[iface]
        else :
            raise Exception('wrong iface -> %s'%(iface))
    def register_handler(self,handler):
        self.update_index()
        print handler
        self.callback_list  = []
        self.basic_check = {'addr_add' : check_ipv4_addr_add,
                               'addr_del' : check_ipv4_addr_del,
                               'link_up' : check_link_up,
                               'link_down' : check_link_down
                               }
#        self.nl.register_callback(nl_evnet_all,lambda x: reg_event_all(x,2),None)
#        return 
        if isinstance(handler,list) == False:
            raise Exception('input item format error')
        for item in handler:
            if len(item) != 4 and isinstance(item,list ) == True :
                raise Exception('input item format error')
            if item[0] == None :                
                print 'add own check function'
                self.nl.register_callback(item[2], lambda x:item[2](x) , item[3])
                print "success register "
                self.callback_list.append(item[2])

            else :
                print "add normal check call"
                if self.keytable.has_key(item[0]) :
                    index =  self.get_index_from_iface(item[0])
                else :
                    raise Exception('input iface error')
                if self.basic_check.has_key(item[1]) :
                    basic_check = self.basic_check[item[1]]
                else :
                    raise Exception('input method  error -> %s'%item)
                input_callback = item[2]
                
                self.nl.register_callback(input_callback, lambda x:basic_check(x,index) ,item[3])
                print input_callback
                print basic_check
                print "success register"
                self.callback_list.append(item[2])
    def unregister_handler(self):
        for item in self.callback_list :
            self.nl.unregister_callback(item)
            print 'un register ok'
                
        

    
def check(x):
    print "private check"
    return True
def check_link_up2(x,index):

    print 'hello6->%s'%index
    return x.get('event', None)=='RTM_NEWLINK' \
        and  x.get('family', None)==0 \
        and x.get('index', None)==index\
        and x.get('__align', None)== 0 \
        and x.get('attrs', None)[2][1]== 'UP'
        
def check_link_down2(x,index):
    print 'hello6->%s'%index
    print index
    return x.get('event', None)=='RTM_NEWLINK' \
        and  x.get('family', None)==0 \
        and x.get('index', None)==index\
        and x.get('__align', None)== 0 \
        and x.get('attrs', None)[2][1]== 'DOWN'
        
def pyroute_register():
    nl = pyroute2.IPRoute()
    ifaces = pyroute2.IPDB(nl = nl, mode = 'direct')
    index = 2
    nl.register_callback(nl_evnet_newlink_up, lambda x:check_link_up2(x,index))
    nl.register_callback(nl_evnet_newlink_down, lambda x:check_link_down2(x,index))
    while  True :
        time.sleep(1)
        index= index+1
    

if __name__ == "__main__" :
#    pyroute2_callback()
    pyroute_register()
    nl_evnet_newlink_up('hello')
    nl_evnet_newlink_down('hello')
    nl_evnet_newaddr_add('hello')
    nl_evnet_newaddr_del('hello')
    test = pyroute_test()
    test.update_index()
    table = [
#                ['p2p1','addr_add',nl_evnet_newaddr_add,None],
#                ('p2p1','addr_del',nl_evnet_newaddr_del,None),
#                ['p2p1','link_up',nl_evnet_newlink_up,None],
                ['p2p1','link_down',nl_evnet_newlink_down,None]

             ]
    pprint.pprint(table) 
    test.register_handler(table)
#    test.unregister_handler()
    while True:
        time.sleep( 1 )
    
