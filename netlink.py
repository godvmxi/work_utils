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
br0_cmd = '''/usr/bin/cpgmgt_methodcall.py -o Ifconfig -m Exec -a "run" '''
ap_cmd = ''' /usr/bin/cpgmgt_methodcall.py -o WIFIAP -m Exec -a "run"  '''
client_cmd = ''' /usr/bin/priority & '''

all = []
RA0 = 'ra0'
ETH0 = 'p32p1'

main = '/etc/netlink/'
wired_link_up = 'wired_link_up'
wired_addr_ready = 'addr_ready'
def get_wifimode():
    return "AP"
    from cpgmgt_service_object import CPGMgt_ConfigDB
    try :
        mode =  CPGMgt_ConfigDB.get_value_of_database(object_name = '/com/cisco/cpg/WiFiMode', key = 'mode',db_file = CPGMgt_ConfigDB.TEMP_CONFIG_DB)
        return mode
    except :
        return "invalid"

def run_dir(path):
    ls = os.listdir(path)
    for tmp in ls :
        print tmp
        tmp = path+'/'+tmp
        cmd = '/bin/bash %s  &' %(tmp)
        logger.info('run script --> %s', cmd)
        print cmd
        os.system(cmd)
def make_run_dir():
    os.system('mkdir -p  %s'%(main))
    os.system('mkdir -p  %s%s'%(main,wired_link_up))
    os.system('mkdir -p  %s%s'%(main,wired_addr_ready))

class func_thread():
    def __init__(self,function,argv):
        pass
        self.lock =  thread.allocate_lock()
        self.func = function
        self.argv = argv
        self.call_num = 0 #call number
        
    def start(self,flag=(True,0)):
        self.call_num+=1
        self.argv = flag
        print self.argv
        thread.start_new_thread(self.thread_function, self.argv)

    def thread_function(self,arg0,arg1):
        try :
            if self.lock.acquire(False) == False:
                print "acquire lock false"
                return
        except :
            print "get lock exception"
            self.lock.release()
#        print "get lock and run"
        self.func(self.argv)
        self.lock.release()
        print 'call num -> %d' %(self.call_num)   

def start_log(clear = False):
    
    if clear :
        os.remove(log_file)        
    file = logging.FileHandler(log_file)  
    logger.addHandler(file) 
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    file.setFormatter(formatter)  
    logger.setLevel(logging.NOTSET)
    logger.info("start netlink monitor")
    return
def check_gateway():
    '''
     set interface priority 
    '''
#    mode = os.popen(''' /usr/bin/cpgmgt_methodcall.py -o WiFiMode -m Get -a "mode"  ''').read()
    mode = get_wifimode()
    logger.info(  mode )

    if mode.find( 'client' ) >  -1 :
        print "client mode"
        logger.info("client mode")
    else :
        print 'not client mode' 
        logger.info("not client mode")
        return
        
    gws_origin =  os.popen('/usr/bin/nm-tool |grep Gateway').readlines()
    logger.info( gws_origin )
    gws = []
    for gw in gws_origin:
        dat = gw.split()
        if len(dat) != 2 :
            logger.error("gw split error")
            return 
        else :
            if __is_valid_ipv4(dat[1]) :
                gws.append(dat[1])
            else :
                print "ipv6 address,do nothing"
                
    if len(gws) != 2:
        print 'not ready to set prrority'
        logger.info('not ready to set prrority')
        return
    
    devs = os.popen('/usr/bin/nm-tool |grep "Device:"').readlines()


    if  len(devs) < 2 :
        return 
    else :
        print 'devs--> ',
        print devs[0]
        
        print 'gws--> ',
        print gws
        dev_1 = devs[0].split()
        dev_2 = devs[1].split()
        print dev_1
        print dev_2
        if dev_1[1] != 'Device:' or dev_2[1] != 'Device:':
            logger.info(  "device can match request" )
            return 

        if dev_1[2] ==  RA0  and dev_2[2] == ETH0 :
            print 'ra0 and p32p1'
            logger.info('ra0 and p32p1')
            
            gateways =  os.popen(''' /sbin/route -n |grep UG |awk '{print $2}' ''').readlines()
            print gateways
            for gw in gateways :
                gw = gw.strip()
                print gw
                if __is_valid_ipv4(gw) :
                    del_gw = 'route del default gw %s' %(gw)
                    os.system(del_gw)
            ra0 = '/sbin/route add default gw %s metric 3 %s' %(gws[0] ,dev_1[2])
            eth0 = '/sbin/route add default gw %s metric 9 %s' %(gws[1] ,dev_2[2])
            print ra0
            logger.info(ra0)
            logger.info(eth0)
            print eth0
            os.system(ra0)
            os.system(eth0)
            return 
        elif dev_1[2] == ETH0 and dev_2[2] == RA0 :
            logger.info('p32p1 and ra0')
            print 'p32p1 and ra0'
            gateways =  os.popen(''' /sbin/route -n |grep UG |awk '{print $2}' ''').readlines()
            for gw in gateways :
                gw = gw.strip()
                print gw
                if __is_valid_ipv4(gw) :
                    del_gw = 'route del default gw %s' %(gw)
                    os.system(del_gw)
            ra0 = '/sbin/route add default gw %s metric 3 %s' %(gws[1] ,dev_2[2])
            eth0 = '/sbin/route add default gw %s metric 9 %s' %(gws[2] ,dev_1[2])
            print ra0
            print eth0
            logger.info(ra0)
            logger.info(eth0)
            os.system(ra0)
            os.system(eth0)
            return 
        else :
            logger.info("do nothing")
            return 
        
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
def exec_br0_run(arg):
    logger.info("run jingliang br0 --> %s  %s "%(arg[0],arg[1]) )
    if arg[0] == False:
        logger.info("just clear br0 data")
        os.system('/sbin/ifconfig br0 0.0.0.0 &')
        os.system('/sbin/ip addr flush dev br0 scope site &')
        os.system('/sbin/ip addr flush dev br0 scope global &')
        os.system('/sbin/ip addr flush dev p32p1 scope site &')
        os.system('/sbin/ip addr flush dev p32p1 scope global &')
        return
    timeout = True
    time.sleep(3)
#    for i in range(1,4) :
#        break;
#        br0 = os.popen(''' cpgmgt_methodcall.py -o WiFiMode -m Get -a "mode" ''').read()
#        logger.info(br0)
#    
##        br0 = os.popen(' /sbin/ifconfig |grep HWaddr |grep br0 ').read()
#        if br0.find("ap") != -1:
##        if len(br0) > 0 and br0.split()[0] == 'br0' :
#          
#            logger.info("run br0 exec run")
#            os.system("/usr/bin/cpgmgt_methodcall.py -o Ethernet -m StartConfig -a True &")
#            os.system(br0_cmd)
#            timeout = False
#    #                time.sleep(2)
#
#        else :
#            print 'loop wait for br0 -> %d'%(i)
#            time.sleep(1)
    br0 = os.popen(''' cpgmgt_methodcall.py -o WiFiMode -m Get -a "mode" ''').read()
    logger.info('????apply wifi mode -> %s' %(br0))
    logger.info("run br0 exec run")
    os.system("/usr/bin/cpgmgt_methodcall.py -o Ethernet -m StartConfig -a True &")
    os.system(br0_cmd)
    logger.info("br0 exit loop for br0 -> %s"%(timeout))
#    time.sleep(4)
    
       
    
def exec_ap_run(arg):
    
    print "run chaojing"
    logger.info("run chaojing")
    for i in range(1,10) :
        ip = os.popen(' ifconfig br0 |grep "inet addr:" ').read()
        logger.info(ip)
        if len(ip) > 0 :
            print 'run ap cmd'
            os.system(ap_cmd)
            return 

        else :
            print 'loop wait fo br0 -> %d'%(i)
            logger.info('loop wait for br0 -> %d'%(i))
            time.sleep(1)
    logger.info("run chaojing false")

def exec_client_priority(arg):
    
    print "run jingliang client"
    logger.info("run jingliang client")
    check_gateway()
    return 
    pid = os.popen('/bin/ps aux |grep -v grep |grep priority ').read()
    logger.info(pid)
    if len(pid ) > 0 :
        logger.info("priority run normally,do nothing")

    else :
        os.system(client_cmd)
        logger.info("priority stopped and start it again")
    logger.info("run jingliang client false")       
    

    

def show_all(lists):
    pprint.pprint(lists)
    statistics  = []
    event = ''
    interface = ''
    state = ''
    family = ''
    flags = 0
    type = 0
    
    for lst in lists :
        type = lst[0]['header']['type']
        event = lst[0]['event']
        family = lst[0]['family']
        flags = lst[0]['flags']
        interface = ''
        state = ''
        index = lst[1]
        attrs = lst[0]['attrs']
        if type == RTM_NEWLINK :
            for attr in attrs :
                if attr[0] == "IFLA_IFNAME" :
                    interface = attr[1]
                if attr[0] == 'IFLA_OPERSTATE':
                    state = attr[1]
        elif type == RTM_DELLINK :
            for attr in attrs :
                if attr[0] == "IFLA_IFNAME" :
                    interface = attr[1]
                if attr[0] == 'IFLA_OPERSTATE':
                    state = attr[1]
                    
        elif type == RTM_NEWADDR:
            
            for attr in attrs :
                if attr[0] == "IFA_LABEL" :
                    interface = attr[1]
                    break
        elif type == RTM_DELADDR:
            
            for attr in attrs :
                if attr[0] == "IFA_LABEL" :
                    interface = attr[1]
                    break            
            
        else :
            interface = ''
            state = ''
        tmp = [index,type,event,family,flags,interface,state]
        statistics.append(tmp)
#    pprint.pprint(lists)
    for s  in statistics :
        print s
        
        
    return
def check_interface_carrier(iface):
    result = os.popen('cat /sys/class/net/%s/carrier' %(iface) ).read()
    if result.find("1") > 0 :
        print "%s is on" %(iface)
        return 1
    elif result.find("0") > 0 :
        print "%s is off" %(iface)
        return 0
    else :
        print "%s state is error" %(iface)
        return -1

class main_loop():
    def __init__(self,group=RTMGRP_LINK |RTMGRP_IPV4_IFADDR,family= NETLINK_ROUTE,log=False):
        IPRoute.groups = RTMGRP_LINK |RTMGRP_IPV4_IFADDR
        IPRoute.groups = RTMGRP_LINK
        IPRoute.family = NETLINK_ROUTE
        self.ip = IPRoute()
#        self.br0_exec_run = func_thread(exec_br0_run,('jingliang','br0 update ip'))
#        self.ap_exec_run = func_thread(exec_ap_run,('chaojing','update ap ip'))
#        self.client_exec_priority = func_thread(exec_client_priority,('jingliang','update client priority') )
        self.all = []
        self.buf = []
        atexit.register(self.exit_func)
        signal.signal(signal.SIGILL, self.exit_func)
        self.counter = 0
        self.log = log
    def exit_func(self):
        print 'process exit'
    def monitor(self):
        self.ip.monitor()
        
        while True :
            self.buf = self.ip.get()
            self.parse_buf(self.buf[0])
            if self.log :
                self.log_for_analyse(self.buf)
                
    def log_for_analyse(self,lst):
         
        tmp = []
        tmp.append(lst)
        tmp.append('index -> %d '%(self.counter))
        self.counter += 1
        tmp.append('time -> %s '%(time.asctime()))
        
        
        self.all.append(object)
    def show_interface(self): 
        print "p32p1 interface state --> %s " % ( os.open(''' cat /sys/class/net/p32p1/carrier''').read() )
        
    def parse_buf(self,dic):
        event = ''
        interface = ''
        state = ''
        family = ''
        flags = 0
    
    
        type = dic['header']['type']
        event = dic['event']
        family = dic['family']
        flags = dic['flags']
        interface = ''
        state = ''
#        logger.info("type -->%s "%(type))
#        logger.info(dic)
        attrs = dic['attrs']
        if type == RTM_NEWLINK :
            for attr in attrs :
                if attr[0] == "IFLA_IFNAME" :
                    interface = attr[1]
                if attr[0] == 'IFLA_OPERSTATE':
                    state = attr[1]
            logger.debug('RTM_NEWLINK -> %s- >%s'%(interface,state))
            if interface == 'br0' and state == 'UP' :
                #br0 up and got ip address
                logger.info('br0 up and set it but do nothing ')

#                self.br0_exec_run.start( ( True,0 ))
            elif interface == "p32p1" and state == "DOWN" :
#                if self.__check_config_lock_state():
#                    logger.info("framework running ,just exit")
#                    return
#                logger.info('p32p1 plug out and unset it,sleep 1 s')
#                self.br0_exec_run.start(( False,0))
                time.sleep(1)
            elif interface == "p32p1" and state == "UP" :
                logger.info('p32p1 plug in and set it')
#                run_dir(main+wired_link_up)
                if self.__check_config_lock_state() :
                    logger.info('framework ifconfig running locked')
                    logger.info('do nothing??')
                    return 
                else :
                    logger.info('just running config')
#                br0_state = os.popen("ifconfig |grep br0").readlines()
#                if len(br0_state) > 0:
                    self.br0_exec_run.start(( True,0 ))
            else :
                return 
                
        elif type == RTM_DELLINK :
            for attr in attrs :
                if attr[0] == "IFLA_IFNAME" :
                    interface = attr[1]
                if attr[0] == 'IFLA_OPERSTATE':
                    state = attr[1]
            logger.debug('RTM_DELLINK -> %s- >%s'%(interface,state))
            if interface == "br0" and interface == "DOWN" :
                logger.info('br0 down and set it')
                os.system(' /sbin/ifconfig  br0  0.0.0.0 ')
                                
        elif type == RTM_NEWADDR:        
            for attr in attrs :
                if attr[0] == "IFA_LABEL" :
                    interface = attr[1]
                    break      
            logger.debug('RTM_NEWADDR -> %s- >%s'%(interface,state))         
            if interface == 'br0'  :
                logger.info('br0 address changged and call wifi ap')
                self.ap_exec_run.start()
                run_dir(main+wired_addr_ready)
                
                
            if interface == 'ra0' or interface == 'p32p1':
                logger.info('ra0 and p32p1 changed and add prority')
                run_dir(main+wired_addr_ready)
                self.client_exec_priority.start()
                    
        else :
            interface = ''
            state = ''
        return
    def __check_config_lock_state(self):
        path = '/tmp/ifconfig.pid.lock'
        if os.path.exists(path) :
            logger.info('ifconfig running !!!!!!!!!!!')
            return True
        else :
            return False
            

            
        
    


if __name__ == '__main__':
    print 'begin monitor netlink'
    
    start_log()
    mode =  get_wifimode()
    print mode
    logger.info('start config mode --> %s'%(mode) )
    make_run_dir()
    logger.info("begin monitor netlink ")
    
    loop = main_loop()
    loop.monitor()
   



    
    
    

