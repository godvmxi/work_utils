#!/usr/bin/env python2.7 
import sys
import atexit
import signal


#if len(sys.argv) < 2:
#    print 'choose program to run, e.g.:'
#    print '%s ip link show' % (sys.argv[0])
#    sys.exit(0)


import pprint
import time
import logging
import random

import subprocess

try:
    import thread
except ImportError:
    import dummy_thread as thread





br0_cmd = '''/usr/bin/cpgmgt_methodcall.py -o Ifconfig -m Exec -a "run" '''
ap_cmd = ''' /usr/bin/cpgmgt_methodcall.py -o WIFIAP -m Exec -a "run"  '''
client_cmd = ''' /usr/bin/priority & '''

all = []
RA0 = 'ra0'
ETH0 = 'p32p1'


log_file = '/var/log/switch_mode.log' 
logger = logging.getLogger() 
file = logging.FileHandler(log_file)  
logger.addHandler(file) 
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
file.setFormatter(formatter)  
logger.setLevel(logging.NOTSET)
mode = ["api set WiFiMode.mode ap",
        "api set WiFiMode.mode client",
        "api set WiFiMode.mode off"
        ]

while True :
    cmd = random.sample(mode,1)
    print cmd
    logger.info(cmd)
    subprocess.Popen(cmd,shell=True)
    
    
    time.sleep(10)
    
    logger.info ( subprocess.Popen("ip addr |grep global ").readlines() )

    
#    subprocess.Popen("api set WiFiMode.mode client")

    
    
    

