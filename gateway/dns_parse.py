#!/usr/bin/env python2.7
# -*- coding:utf-8 -*-
import time
import socket


def resolveHost(host):
    ipDict = {host :[]}
    try:
        results=socket.getaddrinfo(host,None)
        for result in results:
            # print result
            ipDict[host].append( result[4][0] )
            # result[result[4][0]]=host
    except Exception,e:
        print e
    # print ipDict
    return ipDict

if __name__=='__main__':
    start=time.time()
    # print 'starting at: ',start
    resolveHost('189cube.com')
    resolveHost('nosdup.189cube.com')
    resolveHost('nostcp.189cube.com')
    print 'time cost: ',time.time()-start
