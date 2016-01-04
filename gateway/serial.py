#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
__author__ = 'dandan'
#monitor serial status ,and reset the serial port
import serial

class  SerialUtils():
    def __init__(self):
        self.serialHandler = None
        self.readBuf = []
        self.writeBuf = []
        self.writeIndex = 0
        self.readIndex = 0

        pass
    def open(self,com="/dev/ttyUSB0",baudrate=115200):
        self.com =  com
        self.baudrate =  baudrate
        self.serialHandler = serial.Serial(self.com,self.badurate)

        pass
    def close(self):
        pass
    def getTotalBytes(self):
        pass
    def reset(self):
        pass
    def getRawItem(self):
        return "some"
    def writeRawItem(self,raw):
        pass

if __name__ == "__main__" :
    pass