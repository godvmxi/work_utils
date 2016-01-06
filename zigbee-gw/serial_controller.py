#!/usr/bin/env python2.7
import serial
import Queue
import os
import re
import time
class SerialUtils():
    MAX_BUF_SIZE = 512
    def __init__(self):
        buffer= os.popen("ls /dev/ttyUSB*").readlines()
        #print buffer
        self.serialList = []
        self.readQueue  =  Queue.Queue(maxsize = 10)
        self.writeQueue =  Queue.Queue(maxsize = 10)
        self.curReadBuf = ""
        self.curWriteBuf = ""
        self.reStr ='[0-9a-z*#]'
        for item in buffer :
            if item.find("ttyUSB") > 0:
                self.serialList.append(item.replace("\n",""))
        print self.serialList
        print len(self.serialList)
        self.serialHandler = None
        self.logger = None
        pass
    def setLogger(self,logger):
        self.logger = logger

    def open(self,port="/dev/ttyUSB0",baudrate=115200):
        # if port not in self.serialList :
        #     raise Exception("not exist the target usb serial")
        self.port  = port
        self.baudrate =  baudrate
        self.serialHandler =  serial.Serial(self.port,self.baudrate)
        if not self.serialHandler.isOpen():
            raise Exception("Device %s is locked"%self.port)
        self.serialHandler.flushInput()
        self.serialHandler.flushOutput()
        print self.serialHandler

        # self.serialHandler.open()
    def loop(self):
        self.logging( "wait for uart data")
        while True:

            num =  Com.serialHandler.inWaiting()
            if num < 10 :
                time.sleep(0.1)
                #continue
            buf =  Com.serialHandler.read(num)
            if len(buf) != 0:
                pass
                print "in -> %s" %repr(buf)
            else :
                time.sleep(0.01)
                continue
            time.sleep(0.5)

            if not self.stringCheck(buf) :
                self.resetSerial()
                continue
            #     reset com and try read again
            strList =  buf.split("*")
            strListSize =  len(strList)

            indexList =    range(0,strListSize)
            print "list -> %s %s %s"%(strListSize,strList,indexList)
            for index in range(0,strListSize):
                temp = strList[index]
                tempLen = len(temp)
                # print "item -> %d %s"%(tempLen,temp)
                if index == 0 :
                    if tempLen != 0:
                        self.curReadBuf =  "%s%s"%(self.curReadBuf,temp)
                        if (buf[0] != '*' ):
                            # print "index 0 not new "
                            # self.curReadBuf =  "%s%s"%(self.curReadBuf,temp)
                            if tempLen[tempLen-1] == '#':
                                self.readQueue.put('*'+self.curReadBuf)
                                self.curReadBuf = ''
                        else :
                            if temp[tempLen-1] == '#':
                                self.readQueue.put('*'+self.curReadBuf)
                            self.curReadBuf = ""
                    else:
                        # print "index 0 0"
                        if len(self.curReadBuf ) != 0:
                            self.readQueue.put(self.curReadBuf)
                            self.curReadBuf = ""
                elif index == (strListSize-1):
                    # print "last 0 0  ->%d %s"%(tempLen,temp)
                    self.curReadBuf = "%s"%temp
                    # if len(self.curReadBuf ) != 0:
                    if temp[tempLen-1 ] == "#":
                        self.readQueue.put('*'+self.curReadBuf)
                        self.curReadBuf = ''
                    elif len(self.curReadBuf) > self.MAX_BUF_SIZE :
                        self.curReadBuf = ""
                    else :
                        pass



                    # else :
                    #     self.curReadBuf = "*%s"%temp

                    # self.readQueue.put(self.curReadBuf)

                else :
                    # print "normal->%d %s"%(index,temp)
                    self.curReadBuf = "%s"%temp
                    if temp[tempLen-1 ] == "#":
                        self.readQueue.put('*'+self.curReadBuf)
                    elif len(self.curReadBuf) > self.MAX_BUF_SIZE :
                        self.curReadBuf = ""
                    else :
                        pass



            queueSize =  self.readQueue.qsize()
            print "queue size -> %d"%queueSize
            if (queueSize > 3):
                for index in range(0,queueSize):
                    print repr(self.readQueue.get() )
            print
            print

    def logging(self,msg):
        msg = "SerialUtils->%s"%msg
        if self.logger != None :
            self.logger.debug(msg)
        else :
            print(msg)
    def resetSerial(self):
        self.serialHandler.close()
        self.logger('reset serial port')
        time.sleep(0.5)
        self.serialHandler.open()
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
    def stringCheck(self,target):
        flag = True
        for ch in target :
            if ch.isupper() or ch.isdigit() or  ch in ["*","#"]:
                continue
            else :
                flag = False
                break
        return flag

if __name__ == "__main__" :
    reStr =r'[0-9A-Z]'
    test1 = '12345!!'
    test2 = '12345*'
    test3 = '12345#'

    Com =  SerialUtils()
    # Com.open("Com20")
    Com.open()
    Com.loop()
    while True :
        num =  Com.serialHandler.inWaiting()
        if num != 0 :
            print num
        if num < 10 :
            time.sleep(0.1)
            #continue
        test =  Com.serialHandler.read(num)
        if len(test) != 0:
            print repr(test)
        time.sleep(0.5)

    Com.loop()
    pass