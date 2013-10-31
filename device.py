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


from pyroute2.netlink import *
from pyroute2.netlink.generic import *
sock = NetlinkSocket(family=NETLINK_KOBJECT_UEVENT)
sock.bind(1)
counter  = 0
print "hello,socket"
while True:
    test = sock.recv(5000)
    counter = counter +1
    print test



    
    
    

