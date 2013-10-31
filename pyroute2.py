#!/usr/bin/env python
from pyroute2 import IPRoute
ip=IPRoute()
dev=ip.link_lookup(ifname="p7p1")[0]
ip.link('set',index=dev,state='down')