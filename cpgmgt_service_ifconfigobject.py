'''
Created on Mar 25, 2013
@version:    0.1.1
@author:     Jingliang Jiang <jinljian@cisco.com>
'''
import re
from cpgmgt_service_object import *
import subprocess
import shutil
#import os
#import sys
#import shutil

import time
from IPy import IP
import shlex
 
#import common


DEBUG = 1
ADDRESS_SPILT = '/'

ON = '1'
OFF = '0'
PART_ON = '-1'
APKMOD = 'rt5592ap'
STAKMOD = 'rt5592sta'
GE_PCI_ID = '0000:01:00.0'
WIFI_IFNAME = 'ra0'
BRIDGE_IFNAME = 'br0'



NM_IFNAME_NETWORKMANAGER = "org.freedesktop.NetworkManager"
NM_IFNAME_PROPERTIES = "org.freedesktop.DBus.Properties"
NM_IFNAME_ACCESSPOINT = "%s.%s" % (NM_IFNAME_NETWORKMANAGER, "AccessPoint")
NM_IFNAME_DEVICE = "%s.%s" % (NM_IFNAME_NETWORKMANAGER, "Device")
NM_IFNAME_WIRELESS = "%s.%s" % (NM_IFNAME_NETWORKMANAGER, "Device.Wireless")
NM_IFNAME_SETTINGS = "%s.%s" % (NM_IFNAME_NETWORKMANAGER, "Settings")
NM_IFNAME_CONNECTION = "%s.%s" % (NM_IFNAME_NETWORKMANAGER, "Settings.Connection")
NM_IFNAME_CONACTIVE = "%s.%s" % (NM_IFNAME_NETWORKMANAGER, "Connection.Active")
NM_IFNAME_IP4CONFIG = "%s.%s" % (NM_IFNAME_NETWORKMANAGER, "IP4Config")
NM_IFNAME_IP6CONFIG = "%s.%s" % (NM_IFNAME_NETWORKMANAGER, "IP6Config")
NM_IFNAME_DHCP4CONFIG = "%s.%s" % (NM_IFNAME_NETWORKMANAGER, "DHCP4Config")
NM_IFNAME_DHCP6CONFIG = "%s.%s" % (NM_IFNAME_NETWORKMANAGER, "DHCP6Config")
NM_IFNAME_NETWORKMANAGER= "org.freedesktop.NetworkManager"

DHCLIENT_SCRIPT='/usr/bin/dhclient-br0'
BR0_IPV4_LEASES='/var/lib/dhclient/br0_ipv4.leases'
BR0_IPV6_LEASES='/var/lib/dhclient/br0_ipv6.leases'


GE_PCI_ID = '0000:01:00.0'

class UpdateFile():
    ''' update config file class 
    such as :
    key1=value1
    key2=value2
    key3=value3   

    
    The APIs and its shadow function which is not necessary to re-write:
    a. update_line()        #replace one line with key word
    b. remove_line()        #remove one line with key word
    c. read_file()          #manual read file
    d. save_file()          #manual save file
    e. update_lines()       #up one line with key word
    f. show_file()          #whow all lines of file
    
    [key,value]
    if key and value exist ,update value
    if key not exist ,insert a line with key and value
    if value empty ,delete line

    
    Usage:
    usage = UpdateFile('file')
    uasge.read_file()
    uaage.update_lines([ ['key1','value2'],['key2','']  ])

    '''
    
    def __init__(self,name):
        ''' Fake Initialization function
        
        with configure file name
    
        '''
        self.buf = []
        self.split = '='
        self.name = name
 
    def update_line(self,key,value):
        ''' update a line or insert ,if key not exist ,insert ,else update
        
        Args :

            key and value is string
        return :
            True :update
            False :insert        
    
        '''
        tmp = []
        state = False
        for line in self.buf :
            dat = line.split(self.split)
            if dat[0] == key :
                line = '%s=%s\n'%(key,value) 
                state = True #find key and just update line
            tmp.append(line)
        if  state == False: #insert line
            line = '%s=%s\n'%(key,value) 
            tmp.append(line)
            
        self.buf = tmp
        return state
    def remove_line(self,key):
        ''' remove one line with key
        

        value = [key,value]  
        delete line match with key
    
        '''
        tmp = []
        state = False
        for line in self.buf :
            dat = line.split(self.split)
            if dat[0] == key :
                #line = '%s=%s\n'%(value[0],value[1]) 
                state = True #find key and just update line
            else :
                tmp.append(line)
        self.buf = tmp
        return state
    def read_file(self):
        ''' manual read configure file to buf
        
        manual read configure file to buf
    
        '''
        fd = open(self.name)
        self.buf = fd.readlines()
        fd.close()
 
    def save_file(self):
        ''' manual save file
        
        manual save file
    
        '''
        fd = open(self.name,'w')
        fd.writelines(self.buf)
        fd.close()
        

    def update_lines(self,lines):
        self.read_file()
        for line in lines :
            if line[1] == '':
                self.remove_line(line[0])
            else :
                self.update_line(line[0], line[1])
        self.save_file()
    def show_file(self):
        for line in self.buf :
            print line



class CPGMgt_Service_IfconfigObject(CPGMgt_Service_Object):    
    '''Sample DBus Object Class of CPG Management Framework    
    
    API:
        Set "key value "
        Get "key"  
        key   value  example
            wiredIPv4            auto/manual/disable      auto
            wiredIPv6            auto/manual/disable      disable
            wiredAddress4        ipv4/mask                192.168.1.1/255.255.255.0  or 192.168.1.1/24
            wiredAddress6        ipv6/mask                2001::1/64
            wiredGateway4        ipv6                     192.168.1.1
            wiredGateway6        ipv6                     2001::1 
            dns4                 ipv4
            dns6                 ipv6
    return :
        Set key value
    Usage:
        set "wiredIPv4 auto"

    '''
    INIT_CONFIG_VALUE = dbus.Array( [                                      
                                    
                                    ['wiredIPv4','auto'],
                                    ['wiredIPv6','auto'],
                                    
                                    ['wiredAddress4',''],
                                    ['wiredAddress6',''],
                                    ['wiredGateway4',''],
                                    ['wiredGateway6',''],
                                    
                                    ['dns4',''],
                                    ['dns6','']])

    def __init__(self, bus = None, object_path = None): 
        ''' 
        
        init
    
        '''       
        if bus == None :
            bus = dbus.SystemBus();
        if object_path == None :
            object_path = "/com/cisco/cpg/" + "Ifconfig"
        
        self.bus = bus
        self.object_path = object_path
        dbus.service.Object.__init__(self, bus, object_path)
#        self.cpgmgt_log.error("ifconfig init  database")
        self.InitConfig(if_recover = "False",if_temporary = "False")
#        self.cpgmgt_log.error("ifconfig init  database end")
        self.initCfg = self.INIT_CONFIG_VALUE
        self.wifiMode = 'ap'
        self.key = []
        for dat in self.initCfg  :
            self.key.append(dat[0])

        self.runningCfg = self.initCfg
        default_file = '/etc/sysconfig/p32p1.default'
        target_file = '/etc/sysconfig/network-scripts/ifcfg-p32p1'
        if os.path.exists(default_file) == False :
            shutil.copyfile(target_file,default_file)
        else :
            shutil.copyfile(default_file,target_file)
        self.__lock_ifconfig_framework(False)


    def set( self , key , string_array):
        ''' set func
        API:
            Set "key value " 
            key   value  example
                wiredIPv4            auto/manual/disable      auto
                wiredIPv6            auto/manual/disable      disable
                wiredAddress4        ipv4/mask                192.168.1.1/255.255.255.0  or 192.168.1.1/24
                wiredAddress6        ipv6/mask                2001::1/64
                wiredGateway4        ipv6                     192.168.1.1
                wiredGateway6        ipv6                     2001::1 
                dns4                 ipv4
                dns6                 ipv6
        return :
            Set key value
        Usage:
            set "wiredIPv4 auto"
    
        ''' 
#        self.cpgmgt_log.error(type(key))
#        self.cpgmgt_log.error(type(string_array))
        
        if key == 'wifiMode' :
            self.wifiMode = string_array 
            return 'set ' +key + '  ' + string_array       
        try :
            if self.key.count(key) > 0 :
                self.cpgmgt_log.debug(string_array)
            else :
                raise Exception('unexpect key');
        except :
            return 'Wrong key ' + key +'  ' +string_array
        
        #clear memory cache when set to auto
        if self.__check_arg(key, string_array):
            if key == 'wiredIPv4' and   string_array != 'manual' :
                self.SetConfig('wiredAddress4', '', 'True')
                self.SetConfig('wiredGateway4', '', 'True')
                '''
                user can reconfigure the dns to avoid the old dns affect
                '''
                self.SetConfig('dns4', '', 'True')
            if key == 'wiredIPv6' and  string_array != 'manual' :
                self.SetConfig('wiredAddress6', '', 'True')
                self.SetConfig('wiredGateway6', '', 'True')
                self.SetConfig('dns6', '', 'True')
        #clear memory cache when set to auto
                
            
            self.SetConfig(key, string_array, 'True')  # true running  config false start up config
            self.runningCfg = self.GetConfig(None,if_temporary = "True")
        else :
            raise Exception("Wrong format")    
        
        return 'Set ' + key +' '+ string_array;

         

    def get(self, key, string_array = None):
        ''' get value from key
        API:
            Get "key"  
                key                  value                    example
                wiredIPv4            auto/manual/disable      auto
                wiredIPv6            auto/manual/disable      disable
                wiredAddress4        ipv4/mask                192.168.1.1/255.255.255.0  or 192.168.1.1/24
                wiredAddress6        ipv6/mask                2001::1/64
                wiredGateway4        ipv6                     192.168.1.1
                wiredGateway6        ipv6                     2001::1 
                dns4                 ipv4
                dns6                 ipv6
        return :
            key value
        Usage:
            set "wiredIPv4 auto" 
        '''

        self.cpgmgt_log.debug(self.runningCfg)
        if key == 'wifiMode' :
            self.wifiMode = self.__get_wifi_mode()
            return self.wifiMode 
        elif  key == 'mem' :
            return self.runningCfg
        elif key == 'mac' :
            return self.__get_eth0_mac()
        elif key == 'domain' :
            return self.__get_domain()
        elif key == 'bcast' :
            return self.__get_bcast()
        elif self.key.count(key) > 0 :
            return self.__get_network(key)
        else :
            raise Exception("wrong key")
    
    def execute(self, key, string_array = None):
        ''' apply setting 
        args : apply setting 
        key : run

        '''
        self.cpgmgt_log.error("ifconfig run begin")
        self.__lock_ifconfig_framework(False)
        if key == "run" :
            #clear dhclient exit hook file
            self.__remove_dhclient_hooks_file()
            self.__remove_old_leases_file()
            self.__clear_useless_dhclient(False)
            wifiMode = self.__get_wifi_mode()
            #wifiMode = self.GetConfig('wifiMode',if_temporary = "False")
            if wifiMode == 'off' :
                self.cpgmgt_log.error("ifconfig run off")
                return  self.__apply_wifi_mode_off()
            elif wifiMode == 'client' :
                self.cpgmgt_log.error("ifconfig run client")
                return  self.__apply_wifi_mode_sta()
            elif wifiMode == 'ap' :
                self.cpgmgt_log.error("ifconfig run ap")
                return self.__apply_wifi_mode_ap()
            else :
                self.cpgmgt_log.error("wrong wifi mode ,just rescue ")
                self.__apply_rescue_mode()
                raise Exception("wrong wifi mode ,just rescue")
            
            return "Exec run"
        else :
            raise Exception("can not get access wifi mode")

    def __remove_old_leases_file(self):
        os.system("rm -rf /var/lib/dhclient/*  ")

    def __remove_dhclient_hooks_file(self):
        dhcp_hooks = '/etc/dhcp/dhclient-exit-hooks'
        cmd = "/bin/rm -rf %s" %(dhcp_hooks)
        os.system(cmd)
      
    def introspect(self):
        ''' apply show help msg
        

        '''
        usage =  '''
        ifconfig help :
                key:
                
        '''
        return usage

        
    def startconfig(self, if_temporary = "False"):
        ''' start up config 
        args : apply setting 

        '''
        self.cpgmgt_log.error("ifconfig start up begin")
        try:

            self.startupCfg = self.GetConfig(None,if_temporary)
            self.runningCfg = self.startupCfg
            self.cpgmgt_log.debug(self.runningCfg)
            
            counter = 0
            #wifi mode can just decide ,because the wifi mode may be not ready
            while True:
                ifs = os.popen(''' ifconfig br0 ''').readlines()            
                if len (ifs ) == 0:
                    counter = counter +1
                    if counter > 10:
                        self.cpgmgt_log.error("ifconfig start up time out ,can not find br0")
                        break
                    time.sleep(1)
                else :
                    self.cpgmgt_log.debug("ifconfig start up  find br0")
                    break
                
            time.sleep(3)
            self.cpgmgt_log.error("ifconfig start up over")
            self.execute('run')
#            os.system('/usr/bin/python /usr/bin/priority.py ra0 p32p1 &')


        except Exception as inst:
            raise inst
        else:
            return "start config end"


        
    def __is_valid_ipv4(self, ip):
        """
        Validates IPv4 addresses.
        """
        tmp = ip.split('.')
        if len(tmp) != 4 :
            return False
        A = int(tmp[0])
        if A < 1 or A > 223 :
            return False
        B = int(tmp[1])
        if B < 0 or B > 254 :
            return False
        C = int(tmp[2])
        if C < 0 or C > 254 :
            return False
        D = int(tmp[3])
        if D < 0 or D > 254 :
            return False
        return True
    def __is_valid_ipv4_mask(self,mask):
        """Validates IPv4 mask.
        """
        tmp = mask.split('.')
        if len(tmp) != 4 :
            return False
        A = int(tmp[0])
        if A != 255 :
            return False
        B = int(tmp[1])
        if B < 0 or B > 255 :
            return False
        C = int(tmp[2])
        if C < 0 or C > 255 :
            return False
        D = int(tmp[3])
        if D < 0 or D > 254 :
            return False
        return True
    
    def __is_valid_ipv6(self, ip):
        """Validates IPv6 addresses.
        """
        pattern = re.compile(r"""
            ^
            \s*                         # Leading whitespace
            (?!.*::.*::)                # Only a single whildcard allowed
            (?:(?!:)|:(?=:))            # Colon iff it would be part of a wildcard
            (?:                         # Repeat 6 times:
                [0-9a-f]{0,4}           #   A group of at most four hexadecimal digits
                (?:(?<=::)|(?<!::):)    #   Colon unless preceeded by wildcard
            ){6}                        #
            (?:                         # Either
                [0-9a-f]{0,4}           #   Another group
                (?:(?<=::)|(?<!::):)    #   Colon unless preceeded by wildcard
                [0-9a-f]{0,4}           #   Last group
                (?: (?<=::)             #   Colon iff preceeded by exacly one colon
                 |  (?<!:)              #
                 |  (?<=:) (?<!::) :    #
                 )                      # OR
             |                          #   A v4 address with NO leading zeros 
                (?:25[0-4]|2[0-4]\d|1\d\d|[1-9]?\d)
                (?: \.
                    (?:25[0-4]|2[0-4]\d|1\d\d|[1-9]?\d)
                ){3}
            )
            \s*                         # Trailing whitespace
            $
        """, re.VERBOSE | re.IGNORECASE | re.DOTALL)
        return pattern.match(ip) is not None
    def __get_bcast(self):
        mode  =self.__get_wifi_mode()
        if mode == 'ap' :
            cmd = '/sbin/ifconfig br0 |grep "inet addr" '
        else :
            cmd = '/sbin/ifconfig br0 |grep "inet addr "'
        buf = os.popen(cmd).read().split()
        if len(buf) != 4 :
            return ''
        else :
            return buf[2].split(':')[1]

    
    def __get_gateway(self, ty):
        ''' get  gateway 
        args :
            types :gateway4/gateway6
 

        '''
        self.wifiMode = self.__get_wifi_mode()
        
        
        
        if ty == 'gateway4' :
            gw4 = []
            if  self.wifiMode == 'ap' :
                gws = os.popen(''' /sbin/route -n |grep UG|grep br0 | awk '{print $2}' ''').readlines()
            else :
                gws = os.popen(''' /sbin/route -n |grep UG|grep p32p1 | awk '{print $2}' ''').readlines()
            
           
            self.cpgmgt_log.debug('gateway --> %s' %(gws))
            for gw in gws :
                gw4.append(gw.strip())   
            return self.__return_dat_from_list(gw4)
        
        elif ty == 'gateway6':
            gw6 = []
            if  self.wifiMode == 'ap' :            
                ipv6s = os.popen('/sbin/ip -6 route |grep default |grep br0').readlines()
            else :
                ipv6s = os.popen('/sbin/ip -6 route |grep default|grep p32p1').readlines()
            self.cpgmgt_log.debug('gateway --> %s' %(ipv6s))
            if len(ipv6s) >0 :
                for ipv6 in ipv6s :
                    ipv6 = ipv6.split()
                    if len(ipv6) >= 3 :
                        gw6.append(ipv6[2].strip())
            return self.__return_dat_from_list(gw6)

        else:
            self.cpgmgt_log.debug('wrong request')
            return ''
                
            
    def __get_domain(self):
        ''' get dns
        args :
            types :dns4 /dns6
        '''
        domains = os.popen(''' cat /etc/resolv.conf  |grep domain  ''').readlines()
        result = []
        if len (domains )> 0:
            for domain in domains :
                domain = domain.split()
                if len(domain) == 2 and domain[0] == "domain" :
                    result.append(domain[1].strip())
        return self.__return_dat_from_list(result)
 
    def __return_dat_from_list(self,ls):   
#        for l in ls :
#            l = l.replace('\n','')
#            l = l.strip()
        
        ret = []
        for l in ls :
            ret.append(l.strip().replace('\n',''))
        ret = list(set(ret)) 

        d = len(ret)
        
        if d == 0:
            return ''
        elif d == 1 :             
            return ret[0]
        else :
            return ret           

    def __get_interface_dns(self,iface):
        lines = os.popen('nm-tool ').readlines()
        result = []
        tmp = {}
        DNS = []    
        for line in lines :
            if line.find("Device:") > 0:
                if len(tmp) != 0:
                    tmp['dns'] = DNS
                    result.append(tmp)
                    tmp = {}
                    DNS = []
                
                line= line.split()
                tmp['dev'] = line[2]
            else :
                if line.find('DNS') > 0:
        
                    line = line.split()
                    DNS.append(line[1])   
                    
        tmp['dns']= DNS            
        result.append(tmp)
    #    pprint.pprint(result)
        for tmp in result :
            if tmp['dev'] == iface:
                return tmp['dns']
        return []

    def __get_dns(self, ty):
        ''' get dns
        args :
            types :dns4 /dns6
        '''
        result4 = []
        result6 = []
        mode = self.__get_wifi_mode()
        if mode == "ap":
            dnss = os.popen(''' cat /etc/resolv.conf |grep nameserver|awk '{print $2}' ''').readlines()
            result4 = []
            result6 = []
            
            for dns in dnss :
                if self.__is_valid_ipv4(dns) :
                    result4.append(dns)            
                elif  self.__is_valid_ipv6(dns) :
                    result6.append(dns)
                else :
                    self.cpgmgt_log.debug('wrong dns format in  cat /etc/resolv.conf  ->%s '%(dns))
            if ty == 'dns4' :
                return self.__return_dat_from_list(result4)
            elif ty == 'dns6':
                return self.__return_dat_from_list(result6)
            else:
                self.cpgmgt_log.debug('wrong dns request '%(ty))
                return ''
        else :
            dnss = self.__get_interface_dns('p32p1')
            for dns in dnss :
                if  self.__is_valid_ipv4(dns) :
                    result4.append(dns)
                elif self.__is_valid_ipv6(dns):
                    result6.append(dns)
                else :
                    self.cpgmgt_log.debug('wrong dns format in  cat /etc/resolv.conf  ->%s '%(dns))
            if ty == 'dns4' :
                return self.__return_dat_from_list(result4)
            elif ty == 'dns6':
                return self.__return_dat_from_list(result6)
            else:
                self.cpgmgt_log.debug('wrong dns request '%(ty))
                return ''
            

    def __get_address(self, ty):
        ''' get ipaddress 
        args :
            types :wiredAddress4 /wiredAddress6
        '''
        self.wifiMode = self.__get_wifi_mode()
        self.cpgmgt_log.debug('wifimode --> %s' %(self.wifiMode))
        
        if ty == 'wiredAddress4':
            result = []
            if self.wifiMode == 'ap' :
                ip = os.popen(''' /sbin/ifconfig br0 | grep 'inet addr'|awk '{print $2 $4}'  ''').readlines()

            else :
                ip = os.popen(''' /sbin/ifconfig p32p1 | grep 'inet addr'|awk '{print $2 $4}'  ''').readlines()


            if len (ip) > 0 :
                ipmask = ip[0].split('M')

                if len(ipmask ) == 2 :
                    ip = ipmask[0].split(':')[1]
                    mask = ipmask[1].split(':')[1]
                    result.append(   ip +'/'+ mask )
                
            return self.__return_dat_from_list(result)
        elif ty == 'wiredAddress6':
            result = []
            if self.wifiMode == 'ap' :
                ips = os.popen(''' /sbin/ifconfig br0 | grep 'Global'|awk '{print $3}'  ''').readlines()
            else :
                ips = os.popen(''' /sbin/ifconfig p32p1 | grep 'Global'|awk '{print $3}'  ''').readlines()
            if len (ips) > 0 :
                for ip in ips:
                    result.append(ip)
            return self.__return_dat_from_list(result)
        else :
            self.cpgmgt_log.debug('wrong dns request '%(ty))
            return ''


    def __get_eth0_mac(self):
        ''' get mac address  
        the br0 mac maybe changed so i do not get the data
        '''
        mac = os.popen(''' /sbin/ifconfig p32p1 |grep HWaddr| awk '{print $5}' ''').readlines()                
        mac = mac[0]
        mac = mac.strip()
        return mac
    def __get_wired_mode(self,ty):
        return self.__get_value_from_running_cfg(ty)
    
    def __get_network(self, key):
        ''' get network value 
        args :
            types : folowing key in program
 

        '''
        result = {
        'wiredIPv4' :lambda : self.__get_wired_mode('wiredIPv4'),
        'wiredIPv6' :lambda : self.__get_wired_mode('wiredIPv6'),
        'wiredGateway4' :lambda :  self.__get_gateway('gateway4'),
        'wiredGateway6' :lambda : self.__get_gateway('gateway6') ,
        'wiredAddress4' :lambda : self.__get_address('wiredAddress4'),
        'wiredAddress6' :lambda :self.__get_address('wiredAddress6'),
        'dns4' :lambda : self.__get_dns('dns4'),
        'dns6' :lambda : self.__get_dns('dns6')
#        'mac' :lambda :self.__get_eth0_mac()
        
        }[key]()

        return result
    def __check_arg(self, key, value):
        ''' check value valid
        args :
            types : 
        '''
        wifiMode = ['wifiMode']
        ipMode = ['wirelessIPv4','wirelessIPv6','wiredIPv4','wiredIPv6']  #auto /manual /disable
        ipv4 = ['wirelessGateway4','wiredGateway4','dns4']
        ipv6 = ['wirelessGateway6','wiredGateway6','dns6']
        address4 = ['wirelessAddress4','wiredAddress4']
        address6 = ['wirelessAddress6','wiredAddress6']
                                   
        if self.__find_key_in_list(key, wifiMode):
            if value == 'off' or value == 'ap' or value == 'sta' :
                return True
            else :
                raise Exception('Wrong Wifi Mode ')
        elif self.__find_key_in_list(key,ipMode):
            if value == 'auto' or value == 'manual' or value == 'disable' :
                return True
            else :
                raise Exception('Wrong Ip Mode ')
        elif self.__find_key_in_list(key, ipv4):
            if value == '':
                return True
            if self.__get_value_from_running_cfg('wiredIPv4') != 'manual'  and key != 'dns4' :
                raise Exception("set ip must under manual mode")
            
            if key == 'dns4':
                value = value.split()
                for dns in value:
                    if self.__is_valid_ipv4(dns) == False :
                        raise Exception('Wrong dns address ')
                return True
            if self.__is_valid_ipv4(value) :
                return True
            else :
                raise Exception('Wrong Ipv4 address ')
        elif self.__find_key_in_list(key, ipv6):
            if value == '':
                return True
            if self.__get_value_from_running_cfg('wiredIPv6') != 'manual'  and key != 'dns6' :
                raise Exception("set ip must under manual mode")
#            self.cpgmgt_log.debug('check dns6 --> %s'%(value))
            
            
            if key == 'dns6':
                value = value.split()
                for dns in value:
                    if self.__is_valid_ipv6(dns) == False :
                        raise Exception('Wrong dns address ')
                return True
            if self.__is_valid_ipv6(value) :
                return True
            else :
                raise Exception('Wrong Ipv6 address ')
        elif self.__find_key_in_list(key, address4) :
            if value == '':
                return True
            if self.__get_value_from_running_cfg('wiredIPv4') != 'manual' :
                raise Exception("set ip must under manual mode")
            ipMask = value.split(ADDRESS_SPILT)
            if self.__is_valid_ipv4(ipMask[0]) :
                if (len ( ipMask[1]) >2  and self.__is_valid_ipv4_mask(ipMask[1]) ) :
                    return True
                elif (len ( ipMask[1] ) <=2  and int(ipMask[1]) <=32 and int(ipMask[1]) >=0) :
                    return True
                else :
                    raise Exception('Wrong Ipv4 address ')
                return True
            else :
                raise Exception('Wrong Ipv4 address and mask ')
        elif self.__find_key_in_list(key, address6):
            if value == '':
                return True
            if self.__get_value_from_running_cfg('wiredIPv6') != 'manual' :
                raise Exception("set ip must under manual mode")
            ipMask = value.split(ADDRESS_SPILT)
            if self.__is_valid_ipv6(ipMask[0]) :
                if len ( ipMask[1])  >2   :
                    return False
                elif len ( ipMask[1] ) <=2  and int(ipMask[1]) <=64 and int(ipMask[1]) >=0 :
                    return True
                else :
                    raise Exception('Wrong Ipv6 address and address')
                return True
            else :
                raise Exception('Wrong Ipv6 address and mask ')
        else :
            raise Exception('unecpect key ')            
        
        
        return True
    def __find_key_in_list(self , key , lists ):
        ''' get value from running config with key
        '''
        for tmp in lists :
            if key == tmp :
                return True
        return False
    

    def __get_wifi_mode(self):
        ''' get wifi mode from wenbo
        '''
        #self.cpgmgt_log.debug('try to get wifimode')
        reply = self.getconfig(object_name = '/com/cisco/cpg/WiFiMode', key = 'mode', if_temporary = "True")
        #self.cpgmgt_log.debug('try to get wifimode -> %s'%(reply))
        return reply

    def __apply_wifi_mode_off(self):
        ''' apply wifi mode off
        '''
#        os.system('killall priority.py')
        self.__apply_wifi_mode_sta()
        

        return "Exec run off"
    def __clear_interface_state(self,interface,ipv4,ipv6):
        '''
        clear the target interface addr
        can't use ip addr flush to flush the interface utill the kernel 3.5 later
        '''
        if ipv4 :
            buf = os.popen('/sbin/ifconfig %s |grep "inet addr" ' %(interface) ).read()
            if buf == 0:
                #ipv4 not exist
                #do nothing
                pass
            else :
                buf = buf.replace('\n','')
                buf = buf.split()
                if len(buf) != 4 :
                    #ipv4 not exist
                    pass
                else :
                    cmd = '/sbin/ip addr del %s/%s dev %s' %(buf[1].split(':')[1] , buf[3].split(':')[1] ,interface)
                    os.system(cmd)
                    os.system(cmd)
                
        if ipv6 :
            #you can't clear all ipv6 address,which may cause the kernel error on ipv6 stack
            #which will be fix in kernel 3.5 later
            #here just remove global address or do nothing
            #open interface accept_ra
            cmd = '/sbin/ip addr flush dev %s scope global '%(interface)
            os.system(cmd)
            time.sleep(0.5)
            cmd = '/sbin/ip addr flush dev %s scope site '%(interface)
            os.system(cmd)
            time.sleep(0.5)
            cmd = '/sbin/ip addr flush dev %s scope global '%(interface)
            os.system(cmd)
            time.sleep(0.5)
            cmd = '/sbin/ip addr flush dev %s scope site '%(interface)
            os.system(cmd)
            time.sleep(0.5)
#            buf = os.popen(' /sbin/ifconfig %s |grep "inet6 addr" |grep "Global" ' %(interface) ).readlines()
#            if buf == 0:
#                #ipv4 not exist
#                #do nothing
#                pass
#            else :
#                for addr in buf : #may be lot of ipv6 s
#                    addr = addr.replace('\n','').split()
#                    if len(addr) != 4:
#                        #wrong addr
#                        pass
#                    else :
#                        cmd = '/sbin/ip addr del %s dev %s' %(addr[2] ,interface)
#                        os.system(cmd)
#                        os.system(cmd)
            #clear gateway if there is a gateway
            lines = os.popen('/sbin/ip -6 route |grep default |grep %s' %(interface)).readlines()
            for line in lines :
                line = line.split()
                if line[0] == 'default' and line[1]=='via' and line[5]=='metric':
                    del_gw = 'route -A inet6 del default gw %s metric %s  %s' %(line[2],line[6],interface)                        
                    os.system(del_gw)
                    self.cpgmgt_log.erro(del_gw)
                    
                
                
    def __clear_useless_dhclient(self,all_pid):
        '''
        clear dhclient br0 and so on
        '''
        if all_pid :
            os.system('''pkill  -f dhclient ''')
            os.system('''killall dhclient ''')
            time.sleep(0.3)
            
            os.system('''pkill -9 -f dhclient ''')
            os.system('''pkill -9 -f dhclient ''')
            os.system('''killall -9 dhclient ''')
            os.system('''killall -9 dhclient ''')
        else :
            '''just clear dhclient-br0 
             '''
            pids = os.popen(''' /bin/ps aux |grep -v grep |grep dhclient |grep dhclient-br0''' ).readlines()
            for pid in pids :
                pid = pid.split()
                if len(pid) > 2 :
                    cmd = 'kill %s' %(pid[1])
                    os.system(cmd)
                    time.sleep(0.3)
                    cmd = 'kill -9 %s' %(pid[1])
                    os.system(cmd)
            

    def __apply_rescue_mode(self):
        return
        buf = os.popen('ip link show |grep state').readlines()
        br0 = [False,False]
        p32p1 = [False,False]
        ra0 = [False,False]
        for iface in buf :
            iface = iface.replace(':','')
            iface = iface.split()
    def __clear_dns_file(self):
        fd = open("/etc/resolv.conf","w")
        fd.close()    
    def __clear_dhclient_leases(self):
 #       os.system("rm -rf /var/lib/dhclient/*")

        os.system('rm -rf %s'%(BR0_IPV4_LEASES))
        os.system('rm -rf %s'%(BR0_IPV6_LEASES))
    def __lock_ifconfig_framework(self,lock):
        if lock :
            os.system('''/bin/touch  /tmp/ifconfig.pid.lock ''')
        else :
            os.system('''/bin/rm -rf  /tmp/ifconfig.pid.lock ''')

    def __apply_wifi_mode_ap(self):
        ''' apply wifi mode ap
        '''

        self.__clear_interface_state('p32p1',True,True)
        self.__clear_interface_state('ra0',True,True)
        self.__clear_interface_state('br0',True,True)
        self.__clear_useless_dhclient(True)
        self.__clear_dns_file()
        self.__clear_dhclient_leases()


        self.wired = 'br0'
        self.wireless = ''
        ifs = os.popen(''' ifconfig br0 ''').readlines()
        if len (ifs ) == 0:
            #not in wifi mode ,just start p32p1
            self.cpgmgt_log.error('can not find interface br0 ,just start p32p1 to rescue system')
            self.__apply_wifi_mode_sta()

            return "Exec run ap off failed ,start p32p1 for rescue"
        else :
#            self.__set_network_dns()
            self.cpgmgt_log.debug('ifconfig start set br0')

            self.__set_network_ap_dns()
            self.__set_ap_network()
            self.cpgmgt_log.debug('ifconfig time??ifconfig before')


            return "Exec run ap"
        

    def __apply_wifi_mode_sta(self):
        ''' apply wifi mode sta
        '''
#        os.system('priority.py ra0 p32p1 &')
        self.__lock_ifconfig_framework(True)

        self.wired = 'p32p1'
        self.wireless = 'ra0'
        self.wired_cfg_file = '/etc/sysconfig/network-scripts/ifcfg-p32p1'
        self.__set_wired_network()
        self.__set_network_dns()

#        os.system('''   /bin/systemctl restart  NetworkManager.service   ''')
        self.__try_reconnect_interface('p32p1')
        self.__lock_ifconfig_framework(False)
        return "Exec run sta"

    def __get_value_from_running_cfg(self,key):
        ''' get value from running config
        '''
        for item in self.runningCfg :
            if item[0] ==key :
                return item[1]
        raise Exception('can find key in running cfg')
    def __set_wired_network(self):
        ''' set eth0 network
        '''
        eth0_cfg_file = UpdateFile(self.wired_cfg_file)
        value_v4 = self.__get_value_from_running_cfg('wiredIPv4')
        value_v6 = self.__get_value_from_running_cfg('wiredIPv6')
            
        if value_v4 == 'auto' :
            lines = [ ['BOOTPROTO','dhcp'],['IPADDR0',''],['PREFIX0',''],['GATEWAY0',''],['ONBOOT','yes'] ]
            eth0_cfg_file.update_lines( lines )
        elif value_v4 =='manual':
            address4 = self.__get_value_from_running_cfg('wiredAddress4')
            gateway4 = self.__get_value_from_running_cfg('wiredGateway4')
            if address4 == '':
                raise Exception("must set ip in manual mode")
            ip_mask = address4.split('/')
            if len ( ip_mask[1] ) > 2 :
                mask = self.__get_mask_from_ipv4(ip_mask)
            else :
                mask = ip_mask[1];
        #    self.cpgmgt_log.error(address4 +' -> '+ gateway4 +' -> ' + mask)
            eth0_cfg_file.update_lines( [ ['BOOTPROTO','none'],['IPADDR0',ip_mask[0]],['PREFIX0',mask],['GATEWAY0',gateway4 ] ,['ONBOOT','yes'] ] )
        else :

            lines = [  ['BOOTPROTO',''],['IPADDR0',''],['PREFIX0',''],['GATEWAY0',''],['ONBOOT','yes']  ]
            eth0_cfg_file.update_lines(lines)
            print 'do nothing'



            
        if value_v6 == 'auto' :
            lines = [ ['IPV6INIT','\"yes\"'],['IPV6_AUTOCONF','yes'],['IPV6_DEFAULTGW',''],['IPV6ADDR',''],['ONBOOT','yes'] ]
            eth0_cfg_file.update_lines( lines )
        elif value_v6 =='manual':
            address6 = self.__get_value_from_running_cfg('wiredAddress6')
            gateway6 = self.__get_value_from_running_cfg('wiredGateway6')
            if address6 == '':
                raise Exception("must set ip in manual mode")
 
            eth0_cfg_file.update_lines( [ ['IPV6INIT','\"yes\"'],['IPV6_AUTOCONF','no'],['IPV6_DEFAULTGW',gateway6],['IPV6ADDR',address6] ,['ONBOOT','yes']  ] )
        else :
            lines = [  ['IPV6_AUTOCONF','no'] ,['ONBOOT','yes'] ]
            eth0_cfg_file.update_lines(lines)
            #raise Exception("wrong ipv6 mode")
        

    def __get_mask_from_ipv4(self,ip_mask):
        '''  cal net mask to int
        '''
        networkAddress = IP(ip_mask[0]).make_net(ip_mask[1])
        networkAddress = str(networkAddress)
        return networkAddress.split('/')[1]
    def __set_network_dns(self):
        '''  set dns
        '''
        dns4 = self.__get_value_from_running_cfg('dns4')
        dns6 = self.__get_value_from_running_cfg('dns6')
        self.cpgmgt_log.debug('set dns --> %s   %s' %(dns4,dns6) )

        #del origin dns data
        '''
        clear old dns msg
        '''
        cmd = ''' sed '/DNS/d' -i /etc/sysconfig/network-scripts/ifcfg-p32p1 '''
        os.system(cmd)
        dnss=''
        try :
            dnss  =dns4.split() + dns6.split()
        except :
            self.cpgmgt_log.error('ifconfig split dns error')     
        lines = []
        d = len (dnss) 
        print d
        
        if d  != 0 :
            dns = UpdateFile('/etc/sysconfig/network-scripts/ifcfg-p32p1')
            for i in range (0, d) :
                key =  'DNS%d' %(i+1)
                value =  ''.join( dnss[i] )
                line = [key,value]
                lines.append(line)
            self.cpgmgt_log.debug( lines )
            dns.update_lines(lines)
    
    def __update_dhcp_hooks(self,dns4,dns6):
        dhcp_hooks = '/etc/dhcp/dhclient-exit-hooks'
        target = '/etc/resolv.conf'
        lines = ['#!/bin/bash\n',
                 '#dhclp up hooks ,used to insert nameserver after dhclp\n',
                 '#Wriete by :Jingliang\n',
                 '#version v0.2\n'
    
                 ]
        
        lines.append('#last update : %s \n'%(time.asctime() ) )
        
        dnss = dns4.split() + dns6.split()
        for dns in dnss:
            dns = dns.strip()
            dns = dns.lstrip()
            cmd = 'echo "nameserver %s" >> %s \n' %(dns,target)           
            
            lines.append(cmd )
            #in case of the dhclient-script not running
            os.system(cmd)
        '''
        remove the duplicate lines
        '''
        if len(dnss) > 0:
            lines.append('''/bin/sort /etc/resolv.conf |/usr/bin/uniq > /tmp/dhclient_exit_hook_sort\n''')   
            lines.append('''/bin/cp -rf  /tmp/dhclient_exit_hook_sort /etc/resolv.conf\n''')     
#        cmd = 'echo "#modify by dhclient hooks" >> /etc/resolv.conf \n'
#        lines.append(cmd)
        fd = open(dhcp_hooks,'w')
        fd.writelines(lines)
        fd.close()
        os.system('chmod +x %s'%(dhcp_hooks))
            
        
    def __set_network_ap_dns(self):
        '''  set ap dns just in /etc/resolve.conf
            add dhclient exit hook file when the ipv4 and ipv6 mode is diff
        '''
        dns4 = self.__get_value_from_running_cfg('dns4')
        dns6 = self.__get_value_from_running_cfg('dns6') 
        ipv4 = self.__get_value_from_running_cfg('wiredIPv4') 
        ipv6 = self.__get_value_from_running_cfg('wiredIPv6')        
        #update dns to p32p1 config file   

        
        self.__update_dhcp_hooks(dns4,dns6)
        
        if ipv4 == 'auto' and ipv6 == 'auto':
            if dns6 != '' or dns4 != '' :
#            self.cpgmgt_log.error('set dns --> %s   %s' %(dns4,dns6) )
                cmd = ''' sed '/nameserver/d' -i /etc/resolv.conf '''
                os.system(cmd)
                if dns4 != '' :
                    cmd = '/bin/echo \"nameserver %s \"  >> /etc/resolv.conf  ' %(dns4)
                    self.cpgmgt_log.debug(cmd )
                    os.system(cmd)
                if dns6 != '' :
                    cmd = '/bin/echo \"nameserver %s \"  >> /etc/resolv.conf ' %(dns6)
                    self.cpgmgt_log.debug(cmd )
                    os.system(cmd)     
#        else :
#            self.__update_dhcp_hooks(dns4,dns6)
#            return True

    def __set_ap_network(self):
        '''  set ap network 
        '''
        value_v4 = self.__get_value_from_running_cfg('wiredIPv4')
        value_v6 = self.__get_value_from_running_cfg('wiredIPv6')
        address4 = self.__get_value_from_running_cfg('wiredAddress4')
        address6 = self.__get_value_from_running_cfg('wiredAddress6')
        
        gateway4 = self.__get_value_from_running_cfg('wiredGateway4')
        gateway6 = self.__get_value_from_running_cfg('wiredGateway6')
        os.system(''' /usr/bin/killall dhclient ''')


#DHCLIENT_SCRIPT='/sbin/dhclient-br0'
#BR0_IPV4_LEASES='/var/lib/dhclient/br0_ipv4.leases'
#BR0_IPV6_LEASES='/var/lib/dhclient/br0_ipv6.leases'        
            
        if value_v4 == 'auto' :
            cmd = '/sbin/dhclient -4 -sf %s -lf %s br0 &' %(DHCLIENT_SCRIPT,BR0_IPV4_LEASES)
            os.system(cmd)

        elif value_v4 == 'manual' :
            if address4 == '':
                raise Exception("ip address can not be null")
            ip_mask = address4.split('/')
            if len(ip_mask[1]) > 2 :
                cmd = '/sbin/ifconfig br0 inet %s netmask %s' %(ip_mask[0],ip_mask[1] )
            else :
                cmd = '/sbin/ifconfig br0 inet %s' %(address4 )
#            self.cpgmgt_log.error('ifconfig --> %s '%(cmd))
            subprocess.Popen(cmd,shell=True)
            #add ipv4 gateway
            gateways =  os.popen(''' /sbin/route -n |grep UG |awk '{print $2}' ''').readlines()
            for gw in gateways :
                if self.__is_valid_ipv4(gw) :
                    del_gw = 'route del default gw %s' %(gw)
                    os.system(del_gw)
            if gateway4 != '' :
                add_gw = '/sbin/route add default gw %s br0' %( gateway4 ) 
                subprocess.Popen(add_gw,shell=True)
#                self.cpgmgt_log.error('add gateway4 --> %s '%(add_gw))
        else :
            cmd = '/sbin/ifconfig br0  0.0.0.0'
            os.system(cmd)

        if value_v6 == 'auto':
            cmd = 'echo "1" >  /proc/sys/net/ipv6/conf/%s/accept_ra ' %('br0')
            os.system(cmd)
            cmd = '/sbin/dhclient -6 -sf %s -lf %s br0 &' %(DHCLIENT_SCRIPT,BR0_IPV6_LEASES)
            os.system(cmd)
        elif value_v6 == 'manual' :
            
            if address6 == '':
                raise Exception("ip address can not be null")
            
            ipv6s = os.popen(''' /sbin/ifconfig br0|grep Global |awk '{print $2}' ''')
            for ipv6 in ipv6s :
                cmd = '/sbin/ifconfig br0 inet6 del %s' %(ipv6)
                os.system(cmd)
            cmd  = '/sbin/ifconfig br0 inet6 add %s' %(address6)
            os.system(cmd)
            
            #add ipv6 gateway
            #del exist gws about br0            
            gws = os.popen(''' ip -6 route |grep default|grep br0  ''').readlines()
    
            if len(gws) >0 :
                print 'del defualt gw'
                for gw in gws :
                    gw = gw.split()
                    if len(gw) < 7 :
                        print "can find exist gws"
                    else :    
                        
                        del_gw = 'route -A inet6 del default gw %s metric %s  %s' %(gw[2],gw[6],gw[4])                        
                        os.system(del_gw)
                        os.system(del_gw)
            else :
                print 'no exits gws,just add new gateway'
            
            if gateway6 != '' :
                
                add_gw = '/sbin/route -A inet6 add default gw %s br0' %( gateway6 ) 
                os.system(add_gw)

        
        else : #disable ,del all exist ipv6s and gws
            ipv6s = os.popen(''' /sbin/ifconfig br0|grep Global |awk '{print $2}' ''')
            for ipv6 in ipv6s :
                cmd = '/sbin/ifconfig br0 inet6 del %s' %(ipv6)
                os.system(cmd)  
            gws = os.popen(''' ip -6 route |grep default|grep br0  ''').readlines()
    
            if len(gws) >0 :
                print 'del defualt gw'
                for gw in gws :
                    gw = gw.split()
                    if len(gw) < 7 :
                        print "can find exist gws"
                    else :                        
                        del_gw = 'route -A inet6 del default gw %s metric %s  %s' %(gw[2],gw[6],gw[4])
                        
                        os.system(del_gw)         
                    
    def get_eth_ifname_by_pci(self,pci_id):
        ifdir = "/sys/bus/pci/devices/" + pci_id + "/net"
        if not os.path.isdir(ifdir):
            raise Exception("ERROR: Cannot find network interface by PCI ID: {}"\
                    .format(pci_id))
        name = os.listdir(ifdir)
        return name[0]
    
    
    
    def GetMethodInterfaceHandle(self,iface_name, iface_path = None):
        bus = dbus.SystemBus()
        if iface_name[0:1] != '.' and iface_name[0:1] != '/':
            iface_path_tmp = '/' + iface_name.replace('.', '/')
        else :
            iface_path_tmp = iface_name.replace('.', '/')
    
        # Get a proxy for the base NetworkManager object 
        proxy = bus.get_object(NM_IFNAME_NETWORKMANAGER, iface_path_tmp)
        if (iface_path != None) :
            iface = dbus.Interface(proxy, iface_path)
        else:
            iface = dbus.Interface(proxy, iface_name)
    
        return iface
    
    def GetPropertyInterfaceHandle(self,iface_name):
        bus = dbus.SystemBus()
        if iface_name[0:1] != '.' and iface_name[0:1] != '/':
            iface_path_tmp = '/' + iface_name.replace('.', '/')
        else :
            iface_path_tmp = iface_name.replace('.', '/')
    
        proxy = bus.get_object(NM_IFNAME_NETWORKMANAGER, iface_path_tmp)
        iface = dbus.Interface(proxy, NM_IFNAME_PROPERTIES)
        return iface
    
    def __get_interface_dev(self,interface):
        manager = self.GetMethodInterfaceHandle(NM_IFNAME_NETWORKMANAGER)
        devices =  manager.GetDevices()
        print 'interface dev -->%s ' %(interface)
        set_dev = None
        set_state = None
        print "get interface dev"
        for dev in devices :
    
            #    dev.Disconnect()
            
            prop_iface = self.GetPropertyInterfaceHandle(dev)
    
            iface =  prop_iface.Get(NM_IFNAME_DEVICE, "interface")
            print iface
    
            if iface == interface:
                set_dev = dev
                return [True,set_dev,manager]
        return [False,None,None]
    def __get_mac_by_interface(self,interface):
        '''dbus method
        '''
        print "get mac fron %s" %(interface)
        cmd = "ifconfig "+interface +" |grep HWaddr"
        print cmd
        mac = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
        mac = mac.communicate()[0]
        mac = mac.split()
        print mac
        
        if len(mac) == 5:
            mac =  mac[4].split(':')
            print mac
            result = []
            for dat in mac:
                result.append(int(dat,16))
            print result
            return result 
        else :
            return None
    def __get_interface_connection(self,interface):
        '''dbus method
        '''
        print 'interface conn -->%s ' %(interface)
        mac1 = self.__get_mac_by_interface(interface)
        print mac1
        settings_pros = self.GetMethodInterfaceHandle(NM_IFNAME_SETTINGS)
        print settings_pros
        settings = settings_pros.ListConnections()
        print "get interface connect"
        print settings
        for setting in settings :
            
            connect =  self.GetMethodInterfaceHandle(setting, NM_IFNAME_CONNECTION)
    #        print "connect",
    #        print connect
            allSetting =  connect.GetSettings()
    #        print "allSetting",
    #        print allSetting
    
            uuid = allSetting['connection']['uuid']
            mac2 = ""
            try :
                mac2 =  allSetting['802-3-ethernet']['mac-address']
            except :
                print "can't find mac2"
                mac2 = ''
            print mac2
            print 
            if mac2 == mac1 :
                print "find interface"
                return [True,setting]
        print "can't find interface"
        return [False,None]
    def __try_reconnect_interface(self,interface):
        '''renew interface to reload the config file and update ipv6 msg
        '''
#        os.system("ifconfig p32p1 0.0.0.0")
        os.system("ifconfig %s down"%(interface))
        time.sleep(8)
        os.system("ifconfig %s up"%(interface))
        time.sleep(2)
        return



        