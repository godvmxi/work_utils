#!/usr/bin/env  python2.7
import time
import os

class Time():
    def  __init__(self):
        pass
    def setTimeBuf(self,buf):
        pass
    def readRtcTime(self):
        buf =  os.popen("i2cdump -f -y -r 0-15 0 0x51").readlines()
        if len(buf) >= 2 :
            time_buf = buf[1]
        else :
            raise Exception("can not read time from rtc")
        time_buf = time_buf.split()
    return time_buf 
        pass
    def getHostSyncCmd(self):
        pass
    def syncToHost(self):
        pass
    def syncToRtc(self):
        pass
    def getRtcSyncCmds(self):
        pass
def get_rtc_time():
    buf =  os.popen("i2cdump -f -y -r 0-15 0 0x51").readlines()
    time_buf =  None
    if len(buf) >= 2 :
        time_buf = buf[1]
    time_buf = time_buf.split()
    else :
        raise Exception("can not read time from rtc")
    return time_buf 
def set_rtc_time():
    pass
    
def sync_to_host():
    pass
    
def sync_to_rtc():
    pass
if __name__ == "__main__":
    print get_rtc_time()
