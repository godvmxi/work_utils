__author__ = 'Bright Jiang'

import os
import time
import Queue
import pprint
from cmd_define import *

class CmdUtils():
    def __init__(self):
        self.cmdHeader = StructHeader()
        self.headerSize  =  self.cmdHeader.getSize() *2
        self.cmdBody = {}
        self.localPostQueue  = Queue.Queue(maxsize = 20)
        self.remotePostQueue = Queue.Queue(maxsize = 20)
        self.localNetStatus =  True
        self.remoteNetStatus = True
        self.serialHandler =  None
        self.cmdTypeUtils =  CmdTypeUtils()

    def readSerialSerialQueue(self):
        while True :
            #print "try read from serial queue"
            dat = None
            time.sleep(3)
            try :
                dat = self.serialHandler.readItem()
                # print "read S-queue->%s"%dat
            except Exception as inst :
                print ("read serial exception -> %s"%inst)
            if dat !=  None :
                print "read data -> %s"%dat
                if self.localNetStatus :

                    self.localPostQueue.put(dat[1:-1])
                    print "put local queue->%d"%self.localPostQueue.qsize()
                if self.remoteNetStatus :
                    print "put remote queue->%d"%self.remotePostQueue.qsize()
                    self.remotePostQueue.put(dat[1:-1])
            else :
                time.sleep(2)


        pass
    def setHandler(self,handler):
        if handler.has_key("localPost"):
            self.localPostHandler =  handler['localPost']
        else :
            self.localPostHandler =  None
            self.localNetStatus =  False

        if handler.has_key("remotePost"):
            self.remotePostHandler =  handler['remotePost']
        else :
            self.remotePostHandler =  None
            self.remoteNetStatus =  False

        if handler.has_key("localGet"):
            self.localGetHandler =  handler['localGet']
        else :
            self.localPostHandler =  None
            self.remoteNetStatus =  False

        if handler.has_key("remoteGet"):
            self.remoteGetHandler =  handler['remoteGet']
        else :
            self.remoteGetHandler =  None
            self.remoteNetStatus =  False
        if handler.has_key("serial"):
            self.serialHandler =  handler['serial']
            # print "set serial handler -> %s"%self.serialHandler
        else :
            self.serialHandler =  None



    def readPostLocalLoop(self):
        '''
        post add data to postHanderList[0]
        if wwwStatus == Ture ,just post to
        '''

        while True :
            print "read local post queue"
            buf = None
            if not self.localNetStatus :
                self.localPostQueue.get()
                time.sleep(3)
            if self.localPostQueue.qsize() > 0 :
                buf = self.localPostQueue.get()
            else :
                time.sleep(4)
            header =  StructHeader()
            header.loadHex(buf[1:-2])
            jsonData = header.toJson()
            self.localPostHandler.post(jsonData)
    def parseCmdDataFromHex(self,hexBuf):
        headerhex =  hexBuf[:self.headerSize]
        contentHex = hexBuf[self.headerSize:]

        header = StructHeader()
        header.loadHex(headerhex)
        headerDict =  header.toDict()
        bodyDict  ={}
        print "cmd type -->  0x%2X"%header.cmdType
        bodyObject = self.cmdTypeUtils.getCmdDataObject(header.cmdType)
        print "cmd class name ->",self.cmdTypeUtils.getCurClassName()
        if bodyObject != None :
            bodyDict =  bodyObject.toDict()



        # print head.toDict()

        print "cmd type "
        print len(hexBuf),len(headerhex),len(contentHex),self.headerSize
        return [headerDict,bodyDict]
    def readPostRemoteLoop(self):
        '''
        post add data to postHanderList[0]
        if wwwStatus == Ture ,just post to
        '''

        while True :
            time.sleep(4)
            # print "++++++read remote post queue-> %d"%self.remotePostQueue.qsize()
            if not self.remoteNetStatus :
                print "remote net down"
                self.remotePostQueue.get()
                time.sleep(1)
            if self.remotePostQueue.qsize() > 0 :
                buf = self.remotePostQueue.get()
                # print "read from remote queue -> %s"%buf
                result = self.parseCmdDataFromHex(buf)
                if result != None :
                    self.remotePostHandler.post(result[0],result[1])
                    time.sleep(1)
                    # continue
            else :
                time.sleep(4)
    def checkNetworkStatus(self):
        while True :
            if self.localGetHandler.check():
                self.localNetStatus  =  True
            if self.remoteGetHandler.check():
                self.remoteNetStatus =  True
            print "network status -> %d %d"%(self.localNetStatus)
            time.sleep(10)

    def getLocalWriteLoop(self):
        if not self.localNetStatus :
                self.localPostQueue.get()
                time.sleep(1)
    def getRemoteWriteLoop(self):
        while True :
            self.remotePostQueue.get()
            time.sleep(1)


    def parse_header(self,rawData):
        return None
    def parse_contend(self,rawData,cmdType):
        result = {"hello":1}
        return None
    def reset(self):
        self.cmdHeader = {}
        self.cmdBody = {}


