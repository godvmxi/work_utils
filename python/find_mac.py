__author__ = 'bluebird'

import os
import time
import re

fd = open('/var/log/messages','r')
fd.seek(0,2)
# subprocess.call('/sbin/iwpriv ra0 show stainfo',shell=True)
os.system('/sbin/iwpriv ra0 show stainfo')
time.sleep(1)
lines =  fd.readlines()
fd.close
mac_str_re = "([0-9a-fA-F]{2})(([/\s:][0-9a-fA-F]{2}){5})"
mac_list = []
pattern = re.compile(mac_str_re)
for line in lines :
    result =  pattern.search(line)
    if result :
        start = result.start()
        print '111'
        mac_tmp  = line[start:start+17]
        mac_list.append(mac_tmp)
    else :
        print

print mac_list

line = "hello======\r\n"
def find_func(line):

    dat = line.find("=")
    if dat > -1:
        result = ap_string[dat:]
        return result.replace("\n" ,'').replace('\r','')
    else :
        return ""





