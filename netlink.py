#!/usr/bin/env python 
import sys
import atexit
import signal


#if len(sys.argv) < 2:
#    print 'choose program to run, e.g.:'
#    print '%s ip link show' % (sys.argv[0])
#    sys.exit(0)

from pyroute2 import *
from Queue import Empty
from pprint import pprint
from pyroute2.netlink import Netlink

import pprint
import time
from pyroute2.netlink import *
from pyroute2.netlink.generic import *
from pyroute2 import IPRoute

try:
    import thread
except ImportError:
    import dummy_thread as thread


log_file = '/var/log/cpg_netlink.log' 
#RTnetlink multicast groups - backwards compatibility for userspace
RTMGRP_LINK=1
RTMGRP_NOTIFY=2
RTMGRP_IPV4_IFADDR=0x10
RTM_NEWLINK = 16
RTM_DELLINK = 17
RTM_NEWADDR = 20
RTM_DELADDR = 21

logger = logging.getLogger() 


class main_loop():
    def __init__(self,group=RTMGRP_LINK |RTMGRP_IPV4_IFADDR,family= NETLINK_ROUTE,log=False):
        IPRoute.groups = RTMGRP_LINK |RTMGRP_IPV4_IFADDR
        IPRoute.groups = RTMGRP_LINK
        IPRoute.family = family
        self.ip = IPRoute()

        self.counter = 0
        self.log = log

    def monitor(self):
        self.ip.monitor()
        
        while True :
            self.buf = self.ip.get()
            self.parse_buf(self.buf[0])
            print self.buf


if __name__ == '__main__':
    print 'begin monitor netlink'

    logger.info("begin monitor netlink ")
    
    loop = main_loop(family=NETLINK_KOBJECT_UEVENT)
    loop.monitor()
   



    
    
    

