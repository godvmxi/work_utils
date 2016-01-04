#!/usr/bin/env python2.7
import serial
import Queue
import os
class SerialUtils():
    def __init__(self):
        buffer= os.popen("ls /dev/ttyUSB*").readlines()
        #print buffer
        self.serialList = []
        self.readQueue  =  Queue.Queue(maxSize = 10)
        self.writeQueue =  Queue.Queue(maxSize = 10)
        self.curReadBuf = ""
        self.curWriteBuf = ""
        for item in buffer :
            if item.find("ttyUSB") > 0:
                self.serialList.append(item.replace("\n",""))
        print self.serialList
        print len(self.serialList)
        
        pass
    def open(self,port="/dev/ttyUSB0",baudrate=115200):
        if port not in self.serialList :
            raise Exception("not exist the target usb serial")
        self.serial =  serial.Serial(port,baudrate)  
    def loop(self):
        buf = self.serial.readall()
        start = buf.find("*")
        if start == 0:
            if self.curReadBuf[-1] == '#' :
                self.readQueue.put(self.curReadBuf)
                self.curReadBuf = ""
            self.curReadBuf = "%s%s"%(self.curReadBuf,buf[:start]
        stop = buf.find("#")
        
        pass
    def readItem(self):
        if self.readQueue.empty() ==  False :
            return self.readQueue.get()
        else :
            return None
    def writeItem(self,item):
        if self.writeQueue.full() == False :
            self.writeQueue.put(item)
            return True 
        else:
            return False
        pass
        
if __name__ == "__main__" :
    serial =  SerialUtils()
    serial.open()
    serial.loop()
    pass