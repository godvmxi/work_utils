#!/usr/bin/env python

from socket import *
import time
import os
ds5_log_file = "/tmp/ds5/log"
HOST = '<broadcast>'
PORT = 22222
BUFSIZE = 1024
SERVER_IDLE = "(armlmd) IN: \"ult_ds_debugger_ice\" "
SERVER_BUSY = "(armlmd) OUT: \"ult_ds_debugger_ice\" "
INTERFACE = "br0"
def brocast_message(msg) :
    ADDR = (HOST, PORT)

    udpCliSock = socket(AF_INET, SOCK_DGRAM)
    udpCliSock.bind(('', 0))
    udpCliSock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

    udpCliSock.sendto(msg,ADDR)

    udpCliSock.close()
def parse_line(line):
    if line.find(SERVER_IDLE) > -1 :
        return "IDLE"
    elif line.find(SERVER_BUSY) > -1 :
        return "BUSY"
    else :
        return None
def format_message(message_list) :
    print message_list
    return  " -> ".join(message_list)

def get_local_ip(ifname):
    import socket, fcntl, struct 
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    inet = fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15])) 
    ret = socket.inet_ntoa(inet[20:24]) 
    return ret 
def get_server_status():
    cmd =  "ps aux |grep lmgrd |grep 123"
##    return True
    buf = os.popen(cmd).readlines()
    print("app status -> %d ->%s"%(len(buf) ,buf))
    if len(buf) >= 2:
        return True
    else :
        return False

if __name__ == "__main__" :

    local_ip =  get_local_ip(INTERFACE )
    fd =  open(ds5_log_file,'r') 
    lic_server_state =  "IDLE"
    while (True) :
        buf = fd.readline()
        if buf == "" :
            break
        temp = parse_line(buf)
        if temp != None :
            lic_server_state =  temp
    
    if not get_server_status() :
        lic_server_state =  "DOWN"
    message = format_message([local_ip,lic_server_state] )
    brocast_message(message)
    time_out = 0
    while (True) :
        buf = fd.readline()
        if buf == "" :
            time.sleep(10)
            if timeout > 100 :
                print "time out and send heart beat"
                if not get_server_status() :
                    lic_server_state =  "DOWN"
                else :
                    lic_server_state =  "LONG TIME NULL ,MAY BE IDLE"

            else :
                continue
        else :
            temp = parse_line(buf)
            if temp != None :
                lic_server_state =  temp
        
        message = format_message([local_ip,lic_server_state] )
        brocast_message(message)
        