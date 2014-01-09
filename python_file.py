#!/bin/env python
import os


f = open('/tmp/netlink.log','a')
f.write('hello\n')
f.close()
os.system('cat /tmp/netlink.log')