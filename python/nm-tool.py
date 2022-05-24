#!/usr/bin/env python
import shutil
import pprint

import os
def __get_interface_dns(iface):
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

pprint.pprint(__get_interface_dns('p32p1'))        



