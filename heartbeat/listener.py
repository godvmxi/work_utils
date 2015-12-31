#!/usr/bin/env python 
# -*- coding:UTF-8 -*-

from socket import *
from time import ctime

HOST = '127.0.0.1'
PORT = 22222
BUFSIZE = 1024

ADDR = (HOST,PORT)

udpSerSock = socket(AF_INET, SOCK_DGRAM)
udpSerSock.bind(('',PORT))
print 'wating for message...'
while True:
    data, addr = udpSerSock.recvfrom(BUFSIZE)
    print('...received ->%s  %s'%(addr,data) )


udpSerSock.close()
