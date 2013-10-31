#!/bin/env python
#import subprocess 
#import os
import sys
import json
import pprint
ETH0 = 'p2p1'
RA0 = 'ra0'


basic = [
    { "index":1, "vid":0,"hide":1,
     "ap":{"AuthMode":"OPEN","EncrypType":"NONE"}
    },
    { "index":2, "vid":4,"hide":1, 
     "ap":{"AuthMode":"OPEN","EncrypType":"WEP","key_type":"ASCII","key":"00000"}
    },
    { "index":3, "vid":5,"hide":1, 
     "ap":{"AuthMode":"WPAPSK","EncrypType":"AES","key":"cisco1234"}
    },
    { "index":4, "vid":6,"hide":1, 
     "ap":{"AuthMode":"WPA","EncrypType":"AES","radius_ip":"","radius_port":"12345","key":"00000"}
    }
]
advanced = {
            ['SSID1','CISCO_EDGE'],
                                    ['RadioOn','1'],
                                    ['HideSSID','0'],
                                    ['NoForwarding','0'],
                                    ['Channel','11'],
                                    ['HT_OpMode','0'],
                                    ['HT_BW','1'],
                                    ['HT_GI','1'],
                                    ['HT_STBC','0'],
                                    ['HT_MCS','33'],
                                    ['HT_RDG','0'],
                                    ['HT_EXTCHA','0'],
                                    ['HT_AMSDU','0'],
                                    ['HT_AutoBA','1'],
                                    ['HT_BADecline',''],
                                    ['HT_DisallowTKIP','1'],
                                    ['AuthMode','WPAPSK'],
                                    ['EncrypType','AES'],
                                    ['DefaultKeyID','1'],
                                    ['WirelessMode','9'],
                                    ['Key1Type','0'],
                                    ['Key1Str1',''],
                                    ['Key2Type','0'],
                                    ['Key2Str1',''],
                                    ['Key3Type','0'],
                                    ['Key3Str1',''],
                                    ['Key4Type','0'],
                                    ['Key4Str1',''],
                                    ['WPAPSK1','Cisco123'],
                                    ['RADIUS_Server','192.168.2.3'],
                                    ['RADIUS_Port','1812'],
                                    ['RADIUS_Key','ralink'],
                                    ['BGProtection','0'],
                                    ['BeaconPeriod','100'],
                                    ['DtimPeriod','1'],
                                    ['FragThreshold','2346'],
                                    ['RTSThreshold','2347'],
                                    ['TxPower','100'],
                                    ['TxPreamble','0'],
                                    ['ShortSlot','1'],
                                    ['TxBurst','1'],
                                    ['PktAggregate','0'],
                                    ['WmmCapable','0'],
                                    ['APSDCapable','0'],
                                    ['IgmpSnEnable',''],
                                    ['McastPhyMode',''],
                                    ['McastMcs','']
            
            }

ap = {  
        
        'vlan_num':4,
        'ssid1':{ 'en':1, 'vid':3,'hide':1,
                 'ap':{"AuthMode":"OPEN","EncrypType":"NONE"}
                 },
        'ssid2':{ 'en':1, 'vid':4,'hide':1, 
                 'ap':{"AuthMode":"OPEN","EncrypType":"WEP","key_type":"ASCII","key":"00000"}
                 },
        'ssid3':{ 'en':1, 'vid':5,'hide':1, 
                 'ap':{"AuthMode":"WPAPSK","EncrypType":"AES","key":"cisco1234"}
                 },
        'ssid4':{ 'en':1, 'vid':6,'hide':1, 
                 'ap':{"AuthMode":"WPA","EncrypType":"AES",'radius_ip':"","radius_port":"12345","key":"00000"}
                 }
            }

globalVlan = {'vlan_num':4,
        'ssid1':{ 'en':1, 'vid':3,'hide':1,
                 'ap':{"AuthMode":"OPEN","EncrypType":"NONE"}
                 },
        'ssid2':{ 'en':1, 'vid':4,'hide':1, 
                 'ap':{"AuthMode":"OPEN","EncrypType":"WEP","key_type":"ASCII","key":"00000"}
                 },
        'ssid3':{ 'en':1, 'vid':5,'hide':1, 
                 'ap':{"AuthMode":"WPAPSK","EncrypType":"AES","key":"cisco1234"}
                 },
        'ssid4':{ 'en':1, 'vid':6,'hide':1, 
                 'ap':{"AuthMode":"WPA","EncrypType":"AES",'radius_ip':"","radius_port":"12345","key":"00000"}
                 }
            }
wep = {"type":"wep",}
wpa = {}
encrypto = {    
                'OPEN':{"type":'WEP','key_type':"ascii","key":"11111"},
                'SHARED':{"type":'WEP','key_type':"ascii","key":"11111"},
                'WPAPSK':{'type':'AES','key':'cisco1111'},  
                'WPA':{'type':'AES','radius_ip':"","radius_port":"12345","key":""}           
            }
def load_driver():
    return True
def create_ssid(vlan):
    pass    
def generate_vlan(dat) :    
    pass
def set_mutiple_ssid(vlan):
    pass
def set_para(dat):
    print 'set para'
    if isinstance(dat, str) == False :
        print "input dat type"
        return False
    tmp = json.loads(dat)
    if isinstance(tmp, dict) == False:
        print "input dat can not be parsed"
        return False
    try :
        globalVlan['vlan_num'] = tmp['vlan_num']
        for i in range(1, tmp['vlan_num']+1): 
            vlan = 'ssid%s' % (i)
            print "will set vlan  --> %s" %(vlan)
            globalVlan[vlan] = tmp[vlan]    
        return True
    except :
        return False

    
def show_para(dat):
    print json.dumps(dat)
    pprint.pprint(dat)
def check_vlan(vlan):
    try :
        if vlan['en'] != 1 and  vlan['en'] != 0 :
            print 'en flag error'
            return False
        if vlan['hide'] != 1 and  vlan['hide'] != 0 :
            print 'en flag error'
            return False
        print "vlan  en pass " 
        if vlan['vid'] < 0 or vlan['vid'] > 4096 :
            return False
        print "vlan  vid pass " 
        if isinstance(vlan['ap'], dict) :
            return check_encryto(vlan['ap'])
    except :
        print "vlan  check failed " 
        return False
def check_encryto(ap):
    if type(ap) != dict :
        print "check encryto type error"
        return False
    try :
        authMode = ap['AuthMode']
        if authMode == "OPEN" :
            print "auth mode OPEN "
            if len(ap) == 2 and ap["type"] == "NONE":
                print "OPEN NONE mode"
                return True
            elif len(ap) == 3 and ap["type"] == "WEP" :
                if ap["key_type"] == "ASCII" :
                    return True
                elif ap["key_type"] == ["HEX"] :
                    return True
                else:
                    raise "OPEN Wrong key type"
                print "OPEN WEP MODE"
                return True
            else :
                print "OPEN MODE error"
                raise "OPEN MODE DATA ERROR"
                return False
                
        elif authMode == "SHARED" :
            print "auth mode WEP"
            if ap["key_type"] == "ASCII" :
                return True
            elif ap["key_type"] == ["HEX"] :
                return True
            else :
                print "shared mode key type error"
                return False
        elif authMode == "WPA" or authMode == "WPA2" or authMode == "WPA1WPA2" :
            print "auth mode WPA"
            if ap["EncrypType"] == "TKIP" or ap["EncrypType"] =="AES" or ap["EncrypType"] == "TKIPAES" :
                print "WPA encrypto type"
            else :
                print "WPA encrypto mode error"
                return False
        elif authMode == "WPAPSK" or authMode == "WPA2PSK" or authMode == "WPAPSKWPA2PSK" :
            print "auto mode WPAPSK"
        else :
            print "auto mode wrong"
            return True
    except :
        print "check encryto exception"
        return False
            
    return True
def check_input(dat):
    if isinstance(dat, str) == False :
        print "input dat type"
        return False
    tmp = json.loads(dat)
    if isinstance(tmp, dict) == False:
        print "input dat can not be parsed"
        return False
    try :
        if tmp['vlan_num'] > 4 and tmp['vlan_num'] < 1:
            print "vlan id error"
            return False
    except all :
        print "find exception "
        return False

    try :
        for i in range(1, tmp['vlan_num']+1) :
            vlan = "ssid%s" % (i)
            print 'check vlan pass ->  %s  %s ' %(vlan,type(vlan))   
            print dat
            print type(tmp)
            print 'check vlan dat - > %s ' %(tmp[vlan])         
            if check_vlan(tmp[vlan]) != True :
                print "vlan dat error"
                return False
            
        return True
    except :
        print "vlan check except error"
        return False


if __name__ == '__main__':
    if len(sys.argv) != 1 :
        if sys.argv[1] == 'set' :
            set_para(sys.argv[2]) 
    show_para(globalVlan)
    while (True) :
#        global globalVlan
        
        dat = raw_input("input your set data-> ")
        #print "\n your input -->  %s"%(dat)
        state =  check_input(dat) 
        print state
        if state == True:
            print set_para(dat)
        show_para(globalVlan)



