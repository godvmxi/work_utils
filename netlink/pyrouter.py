__author__ = 'bluebird'
import time
import pyroute2
netlink = pyroute2.IPRoute()

nl = pyroute2.IPRoute()
#ifaces = pyroute2.IPDB(nl, mode = 'direct')
while True:
    print nl.get()



