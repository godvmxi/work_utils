#!/bin/env python
__author__ = 'bluebird'
from cpgmgt_client_object import CPGMgt_Client_Object
import  pprint
import json
import  os

def wifista_get_mac():
    buf = os.popen("ip link show dev ra0 |grep ether |awk '{print $2}' ").read()
    buf = buf.strip()
    print 'get Mac--->%s<--'%(buf)
    return buf


Station = '/com/cisco/cpg/Network/WiFiSta/Client'


wifista_get_mac()

client = CPGMgt_Client_Object()

reply = client.method_call_native(Station, None, "Get", "active0", "link")
print "Get Station --->%s<---"%reply





print type(reply)
if len(reply) != 0 :
    reply = json.loads(reply)
    print type(reply)
    pprint.pprint(reply)

reply = client.method_call_native(Station, None, "Get", "active0", "ap")
print 'ap data --->'+reply
if len(reply) != 0 :
    reply = json.loads(reply)
    print type(reply)
    pprint.pprint(reply)

