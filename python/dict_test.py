#!/bin/env python


dicts={"a":1,"b":2}
for key in dicts:
    print key
    print dicts[key]
    print type(key)
    print type(dicts[key])
    
#dicts.pop('a')
print dicts.has_key('c')


for (k,v) in  dicts.items():
    print k
    print v
    print type(k)
    print type(v)


