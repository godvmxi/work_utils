#!/usr/bin/python

import socket
import struct

def dhcppacket():
    msgtype = 11
    transid = 4711
    c = struct.pack("!BBH", msgtype, 0, transid)
    c = c + struct.pack("!HHH", 6, 2, 0x17)
    return c

def printv6(a):
    print "nameserver %x:%x:%x:%x:%x:%x:%x:%x" % a
    
HOST = 'ff02::1:2' # The remote host
PORT = 547 # The same port as used by the server
LISTENPORT = 546
s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
ls = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
ls.bind(('', LISTENPORT))
p = dhcppacket()
s.sendto(p, 0, (HOST, PORT))
s.sendto(p, 0, (HOST, PORT))
s.sendto(p, 0, (HOST, PORT))
s.sendto(p, 0, (HOST, PORT))
s.sendto(p, 0, (HOST, PORT))
s.close()
print "wait to receive"
data = ls.recv(1024)
(a, b, c) = struct.unpack('!BBH', data[0:4])
data = data[4:]
while data:
    (type, length) = struct.unpack('!HH', data[:4])
    data = data[4:]
    payload = data[:length]
    if type == 23:
        while payload:
            printv6(struct.unpack('!HHHHHHHH', payload[:16]))
            payload = payload[16:]
            data = data[length:]