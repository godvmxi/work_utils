#!/bin/env python
import json
obj = [[1, 2, 3], 123, 123.123, 'abc', {'key1':[1, 2, 3], 'key2':[4, 5, 6]}]
encodedjson = json.dumps(obj)
print repr(obj)
print encodedjson


vlan = {'vlan_num':4,      
        'vlan1':{ 'enable':True, 'vid':"     ",'ap':{}},
        'vlan2':{ 'enable':True, 'vid':4,'ap':{}},
        'vlan3':{ 'enable':True, 'vid':5,'ap':{}},
        'vlan4':{ 'enable':True, 'vid':6,'ap':{}}
        }

random = (5, [1, 2], "tom\" is good", (1, 2), 1.5, True, None)
jsonObj = json.dumps(vlan)
load = json.loads(jsonObj)
print 'dumps-->',jsonObj
print 'load-->',load
print type(jsonObj)
print type(load)
print json.dumps([1  ,  2,    3,{'4': 5, '6': 7}], separators=(',', ':'))


test = '''  hello'ooo'kkk'''
print jsonObj
print jsonObj.replace(" ", '')

dns1 = {  'primary' :'8.8.8.8',
            'secondary' :''
        }
dns2 = {  'primary' :'8.8.8.8',
            'secondary' :'9.9.9.9'
        }
dns3 = {  'primary' :'',
            'secondary' :'9.9.9.9'
        }
dns4 = {  'primary' :'',
            'secondary' :''
        }

print
print
print "'"+ json.dumps(dns1, separators=(',', ':'))  + "'"
print "'"+ json.dumps(dns2, separators=(',', ':'))  + "'"
print "'"+ json.dumps(dns3, separators=(',', ':'))  + "'"
print "'"+ json.dumps(dns4, separators=(',', ':'))  + "'"





