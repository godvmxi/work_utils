#!/usr/bin/env python
'''
@brife:
    switch network interface priority , the network flow will go through the the high prroprity  interface 
    
@Created on June 13, 2013

@author:  Jingliang <jinljian@cisco.com>

'''


import sys
import traceback

import gobject

import dbus
import dbus.mainloop.glib
import pdb
import re
import os
import time
import datetime

global index
from IPy import IP

#RA0 = 'ra0'
#ETH0 = 'p32p1'

RA0 = 'ra0'
ETH0 = 'p32p1'

  
def check_gateway():
    '''
     set interface priority 
    '''
    gws =  os.popen('/usr/bin/nm-tool |grep Gateway').read()
    print gws
    gws = gws.split()
    if len(gws) != 4:
        print 'not ready to set prrority'
        return False
    
    devs = os.popen('/usr/bin/nm-tool |grep "Device:"').read()
    print devs
    print 'len --> %d  %d' %(len(gws),len(devs))
    devs = devs.split()
    if  len(devs) != 10 :
        return False
    else :
        print 'devs--> ',
        print devs
        
        print 'gws--> ',
        print gws
        

        if devs[2] ==  RA0  and devs[7] == ETH0 :
            
            gateways =  os.popen(''' /sbin/route -n |grep UG |awk '{print $2}' ''').readlines()
            for gw in gateways :
                gw = gw.strip()
                print gw
                if __is_valid_ipv4(gw) :
                    del_gw = 'route del default gw %s' %(gw)
                    os.system(del_gw)
            ra0 = '/sbin/route add default gw %s metric 1 %s' %(gws[1] ,devs[2])
            eth0 = '/sbin/route add default gw %s metric 9 %s' %(gws[3] ,devs[7])
            print ra0 
            print eth0
            nets = os.popen( ''' ''')
            os.system(ra0)
            os.system(eth0)
            return True
        elif devs[2] == ETH0 and devs[7] == RA0 :
            gateways =  os.popen(''' /sbin/route -n |grep UG |awk '{print $2}' ''').readlines()
            for gw in gateways :
                gw = gw.strip()
                print gw
                if __is_valid_ipv4(gw) :
                    del_gw = 'route del default gw %s' %(gw)
                    os.system(del_gw)
            ra0 = '/sbin/route add default gw %s metric 1 %s' %(gws[3] ,devs[7])
            eth0 = '/sbin/route add default gw %s metric 9 %s' %(gws[1] ,devs[2])
            os.system(ra0)
            os.system(eth0)
            return True
        else :
            return False
            raise Exception("can find right interface")
    
    return True
    if  len(gws) != 4 or gws[1] == '0.0.0.0'  or gws[3] == '0.0.0.0' :
        return False
    else :
        devs = os.popen('/usr/bin/nm-tool |grep "Device:"').read()
        print devs
        
def __is_valid_ipv4(ip):
    """Validates IPv4 addresses.
    """
    pattern = re.compile(r"""
        ^
        (?:
          # Dotted variants:
          (?:
            # Decimal 1-255 (no leading 0's)
            [3-9]\d?|2(?:5[0-5]|[0-4]?\d)?|1\d{0,2}
          |
            0x0*[0-9a-f]{1,2}  # Hexadecimal 0x0 - 0xFF (possible leading 0's)
          |
            0+[1-3]?[0-7]{0,2} # Octal 0 - 0377 (possible leading 0's)
          )
          (?:                  # Repeat 0-3 times, separated by a dot
            \.
            (?:
              [3-9]\d?|2(?:5[0-5]|[0-4]?\d)?|1\d{0,2}
            |
              0x0*[0-9a-f]{1,2}
            |
              0+[1-3]?[0-7]{0,2}
            )
          ){0,3}
        |
          0x0*[0-9a-f]{1,8}    # Hexadecimal notation, 0x0 - 0xffffffff
        |
          0+[0-3]?[0-7]{0,10}  # Octal notation, 0 - 037777777777
        |
          # Decimal notation, 1-4294967295:
          429496729[0-5]|42949672[0-8]\d|4294967[01]\d\d|429496[0-6]\d{3}|
          42949[0-5]\d{4}|4294[0-8]\d{5}|429[0-3]\d{6}|42[0-8]\d{7}|
          4[01]\d{8}|[1-3]\d{0,9}|[4-9]\d{0,8}
        )
        $
    """, re.VERBOSE | re.IGNORECASE)
    return pattern.match(ip) is not None

def catchall_plug_signals_handler(para):
    print para

def catchall_hello_signals_handler(hello_string):
    '''
    network after dhcp handler
    '''
#    pdb.set_trace()
    print "Received a hello signal and it says " 
    try :

        print hello_string[dbus.String('State')]

        if hello_string[dbus.String('State')] == 2:
            print 'dhcp ok and try to set the metric'
            check_gateway()
    except KeyError:
        print 'ignore this state'
def usage():
    '''
    show help mesage
    '''
    usage = '''
    switch network interface priority , the network flow will go through the the high prroprity  interface 
    usage : interface_priority dev_high dev_low or para null
        dev_high   -> ra0 (defaut)
        dev_high   -> p32p1 (defaut)        
    you can run route -n to check the priority    
    '''
    print usage
    exit()
    pass
def version():
    '''
    show version mesage
    '''
    version = '''  0.1 beta '''
    print version
    exit()
    pass

if __name__ == '__main__':
    

    
    argc = len(sys.argv)

    if argc == 3:
        RA0 = sys.argv[1]
        ETH0 = sys.argv[2]
    elif argc == 2 :
        if sys.argv[1] == '--version' or sys.argv[1] == '-v' :
            version()
        else :
            usage()
    elif argc == 1  :
        pass
    else :
        usage()
        
        
    import logging 
    logger = logging.getLogger() 
    file = logging.FileHandler("qqxml.log")  
    logger.addHandler(file) 
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    file.setFormatter(formatter)  
    logger.setLevel(logging.NOTSET)  
    while True :
        logger.info(time.asctime( ) + "dandan")
        time.sleep(2)
        
    print RA0 
    print ETH0
    
    print 
    
    ifcfg_p32p1 = [
'''nihao  ''',
'''nihao  ''',
'''nihao  ''',
'''nihao  ''',
'''nihao  ''',
'''nihao  '''
]
    config_target = '/home/bluebird/p32p1'
    fd = open(config_target,'w')
    fd.write(ifcfg_p32p1)
    fd.close()
    fd = open(config_target)
    print fd.read()
    exit()
    
    
    dns4 = '8.8.8.8 8.8.4.4'
    dns6= '2001::1 2001::2'

    dhcp_hooks = '/nfs/dhcp-up-hooks'
    target = '/etc/resolv.conf'
    lines = ['#!/bin/bash\n',
             '#dhclp up hooks ,used to insert nameserver after dhclp\n',
             '#Wriete by :Jingliang\n'

             ]
    lines.append('#last update : %s \n'%(time.asctime() ) )
    
    dnss = dns4.split() + dns6.split()
    for dns in dnss:
        lines.append('echo "nameserver  %s" >> %s \n' %(dns,target) )
    fd = open(dhcp_hooks,'w')
    fd.writelines(lines)
    fd.close()
    os.system('chmod +x %s'%(dhcp_hooks))

    
    exit()
    
    

    
    print 'first run to check gateway'
    check_gateway()  
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    bus = dbus.SystemBus()
    #check_gateway()
    bus.add_signal_receiver(catchall_hello_signals_handler, dbus_interface = "org.freedesktop.NetworkManager.Connection.Active", signal_name = "PropertiesChanged")
    bus.add_signal_receiver(catchall_plug_signals_handler, dbus_interface = "org.freedesktop.NetworkManager.Device.Wired", signal_name = "PropertiesChanged")
    
    loop = gobject.MainLoop()
    loop.run()
    



                
            
            
