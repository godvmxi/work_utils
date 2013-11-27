#!/bin/env python
import pyroute2
#from pyroute2 import IPRoute
import time
import sys
import os
import pprint
import warnings


    
def nl_evnet_newlink_up(msg):
    print '%s--> %s'%(sys._getframe().f_code.co_name,0)
def nl_evnet_newlink_down(msg):
    print '%s--> %s'%(sys._getframe().f_code.co_name,0)
def nl_evnet_newroute_add(msg):
    print '%s--> %s'%(sys._getframe().f_code.co_name,0)
def nl_evnet_newroute_del(msg):
    print '%s--> %s'%(sys._getframe().f_code.co_name,0)
def nl_evnet_newaddr_add(msg):
    print '%s--> %s'%(sys._getframe().f_code.co_name,0)
def nl_evnet_newaddr_del(msg):
    print '%s--> %s'%(sys._getframe().f_code.co_name,0)
def nl_evnet_all(msg):
    print '%s->%s'%(msg.get('event'),msg)

class nl_callback_object():
    
    def __init__(self,iface_index = 0,check_action = None,callback = None):
#        print "init"
        self.iface_index  = iface_index
        self.msg = None
        self.__callback_handler = callback
        self.options = {'addr4_add' : self.__check_addr4_add__,
                               'addr4_del' : self.__check_addr4_del__ ,
                               'link_up' : self.__check_link_up__ ,
                               'link_down' : self.__check_link_down__
                               }
        if self.options.has_key(check_action):
            self.___check_handler = self.options[check_action]
        elif callable(check_action) :
            self.___check_handler = check_action
        else :
            self.___check_handler = self.__check_default__        
        print self.iface_index,self.__callback_handler,self.___check_handler
         
    def check_and_call(self,msg):
        if self.___check_handler(msg,self.iface_index) :
            self.__callback_handler(msg)
    def __check_addr4_add__(self,msg,iface_index):
        return  msg.get('index') == iface_index \
        and  msg.get('event') =='RTM_NEWADDR' \
        and msg.get('family') == 2
    def __check_addr4_del__(self,msg,iface_index):
        return msg.get('index') == iface_index \
        and msg.get('event') =='RTM_DELADDR'\
        and msg.get('family') == 2
    def __check_link_up__(self,msg,iface_index):
        return msg.get('event')=='RTM_NEWLINK' \
        and  msg.get('family')==0 \
        and msg.get('index')==iface_index\
        and msg.get('__align')== 0 \
        and msg.get('attrs')[2][1]== 'UP'
 
    def __check_link_down__(self,msg,iface_index):
        return msg.get('event')=='RTM_NEWLINK' \
        and  msg.get('family')==0 \
        and msg.get('index')==iface_index\
        and msg.get('__align')== 0 \
        and msg.get('attrs')[2][1]== 'DOWN'
   
    def __check_default__(self,msg,iface_index):
        return False   

class pyroute_test():
    def __init__(self):
        self.BRIDGE_IFNAME = 'br0'
        self.GE_IFNAME = 'p32p1'
        self.WIFI_IFNAME = 'ra0'
        self.nl = pyroute2.IPRoute()
        self.ifaces = pyroute2.IPDB(nl = self.nl, mode = 'direct')

        
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

    def get_index_from_iface(self,iface):
        try :
            return self.ifaces.get(iface)['index']
        except Exception as inst :
            raise Exception("get can the iface index --> %s  %s"%(iface,inst))
        
        if self.keytable.has_key(iface) :
            return self.keytable[iface]
        else :
            raise Exception('wrong iface -> %s'%(iface))
    @staticmethod          
    def nl_event_handler(msg,obj,arg=None):
        obj.check_and_call(msg)

#        arg[0].check_and_call(msg)
    def register_handler(self,handler):

        self.callback_list  = []
        monitor_event = ['RTM_DELADDR','RTM_NEWLINK','RTM_NEWADDR']

        if isinstance(handler,tuple) == False:
            raise Exception('input item format error')
        for item in handler:
            if len(item) != 4 and isinstance(item,list ) == True :
                raise Exception('input item format error')
            else :
             
                index = self.get_index_from_iface(item[0])
                tmp = nl_callback_object(iface_index = index,check_action=item[1],callback=item[2])                            
                
                self.nl.register_callback(self.nl_event_handler, 
                            lambda x:x.get('event') in monitor_event  ,
                            (tmp,item[3]))
#                print "register-> %s"%(item)
                self.callback_list.append(item[2])
    
        
    def register_handler2(self,handlerTable):
        self.update_index()
        print handlerTable


        self.nl.register_callback(self.nl_event_handler, lambda x:(x.get('event') in ['RTM_DELADDR','RTM_NEWLINK','RTM_NEWADDR'] ) ,args=tuple( handlerTable))

    def unregister_handler(self):
        for item in self.callback_list :
            self.nl.unregister_callback(item)
            print 'un register ok'
    

        



if __name__ == "__main__" :
    nl_evnet_newlink_up('hello')
    nl_evnet_newlink_down('hello')
    nl_evnet_newaddr_add('hello')
    nl_evnet_newaddr_del('hello')
    test = pyroute_test()
    table = (
#                ['p2p1','addr_add',nl_evnet_newaddr_add,None],
#                ('p2p1','addr_del',nl_evnet_newaddr_del,None),
                ['br0','addr4_add',nl_evnet_newaddr_add,None],
                ['br0','addr4_del',nl_evnet_newaddr_del,None],
                ['p32p1','link_up',nl_evnet_newlink_up,None],
                ['p32p1','link_down',nl_evnet_newlink_down,None],

             )
#    pprint.pprint(table) 
    test.register_handler(table)
#    test.unregister_handler()
    while True:
        time.sleep( 1 )
    
