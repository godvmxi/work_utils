#!/bin/env python
import pyroute2
#from pyroute2 import IPRoute
import time
import sys
import os



'''
RTM_DELADDR
'''
p2p1 = 1
def reg_ipv4_addr_add(x):
    return x.get('index', None) == p2p1 and x.get('event', None) =='RTM_NEWADDR' and x.get('family') == 2
def reg_ipv4_addr_del(x):
    return x.get('index', None) == p2p1 and x.get('event', None) =='RTM_DELADDR'and x.get('family') == 2

def reg_link_up(x):
    return x.get('index', None) == p2p1 and x.get('event', None) =='RTM_SETLINK' and x.get('family') == 0
def reg_link_down(x):
    return x.get('index', None) == p2p1 and x.get('event', None) =='RTM_SETLINK' and x.get('family') == 2


def reg_new_route_ipv4(x):
    return x.get('event', None)=='RTM_NEWROUTE' and  x.get('family', None)==2
def reg_new_route_ipv6(x):
    return x.get('event', None)=='RTM_NEWROUTE' and  x.get('family', None)==10


def reg_new_link_up(x):
    return x.get('event', None)=='RTM_NEWLINK' and  x.get('family', None)==0 and x.get('index', None)==p2p1
def reg_new_link_down(x):
    return x.get('event', None)=='RTM_NEWLINK' and  x.get('family', None)==0 and x.get('index', None)==p2p1


    
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

#mon = pyroute2.IPRoute()
#mon.register_callback(nl_event_link0,lambda x:ipv4_addr_add(x) ,None)
#mon.register_callback(nl_evnet_link1,lambda x:ipv4_addr_del(x) ,None)
#mon.register_callback(nl_evnet_link1,lambda x: x.get('index', None) == 1,None)
#mon.register_callback(nl_evnet_link2,lambda x: x.get('index', None) == 2,None)
#mon.register_callback(nl_evnet_link3,lambda x: x.get('index', None) == 3,None)
#mon.register_callback(nl_evnet_link4,lambda x: x.get('famliy', None) == 2,None)
#mon.register_callback(nl_evnet_link5,lambda x: x.get('famliy', None) == 10,None)
#mon.register_callback(nl_evnet_link6,lambda x: x.get('event') is not None,None)



#mon.register_callback(nl_evnet_newaddr_add,lambda x: reg_ipv4_addr_add(x),None)
#mon.register_callback(nl_evnet_newaddr_del,lambda x: reg_ipv4_addr_del(x),None)
#mon.register_callback(nl_evnet_newroute_add,lambda x: reg_new_route_ipv4(x),None)
#mon.register_callback(nl_evnet_newroute_del,lambda x: reg_new_route_ipv6(x),None)
#mon.register_callback(nl_evnet_newlink_up,lambda x: reg_new_link_up(x),None)
#mon.register_callback(nl_evnet_newlink_down,lambda x: reg_new_link_down(x),None)


#mon.register_callback(nl_evnet_all,lambda x: x.get('event') is not None,None)
#while(True):
#    time.sleep(10)
class pyroute_test():
    def __init__(self):
        self.BRIDGE_IFNAME = 'br0'
        self.GE_IFNAME = 'p32p1'
        self.WIFI_IFNAME = 'ra0'
        pass
#        self.bridge = ''
#        self.ifaces = ''
#        self.nl = ''
        
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
        

if __name__ == "__main__" :
    test = pyroute_test()
    test.test()
    
        

