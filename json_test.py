#!/bin/env python
import json
obj = [[1, 2, 3], 123, 123.123, 'abc', {'key1':[1, 2, 3], 'key2':[4, 5, 6]}]
encodedjson = json.dumps(obj)
print repr(obj)
print encodedjson


vlan = {'vlan_num':4,      
        'vlan1':{ 'enable':True, 'vid':3,'ap':{}},
        'vlan2':{ 'enable':True, 'vid':4,'ap':{}},
        'vlan3':{ 'enable':True, 'vid':5,'ap':{}},
        'vlan4':{ 'enable':True, 'vid':6,'ap':{}}
        }

random = (5, [1, 2], "tom\" is good", (1, 2), 1.5, True, None)
jsonObj = json.dumps(vlan)
load = json.loads(jsonObj)
print jsonObj
print load
print type(jsonObj)
print type(load)


for i in range(1,3) :
    print i
