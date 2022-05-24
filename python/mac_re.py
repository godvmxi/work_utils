__author__ = 'bluebird'
import re
bufs ='''
2014-01-20T18:13:19.786466+08:00 CE340 kernel: [ 8617.107320] 00:24:D7:C7:14:B8  1   0   0   1   3       -43    -71    0      HTMIX     40M   15    0     0     247    270    4210      , 4210, 0%
'''
mac_str_re = "([0-9a-fA-F]{2})(([/\s:][0-9a-fA-F]{2}){5})"
print mac_str_re
pattern = re.compile(mac_str_re)
result  = pattern.search(bufs)
print result
start  = result.start()
print type(start)
print bufs[start:start+17]
