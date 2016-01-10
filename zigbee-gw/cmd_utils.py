__author__ = 'Bright Jiang'

import os
import time
import Queue
from struct_base import *
class CmdTypeDefine():
    cmd_node_setup_requset          = 0x01
    cmd_node_setup_para_set         = 0x02
    cmd_active_controller_set       = 0x04
    cmd_action_collect              = 0x05
    cmd_node_working_para_request   = 0x06
    cmd_controller_para_set         = 0x07
    cmd_switch_papa_set             = 0x08
    cmd_server_check_time           = 0x09
    cmd_node_permisson_set          = 0x0A
    cmd_force_node_regist           = 0x0B
    cmd_switch_state                = 0x0C
    cmd_controller_state            = 0x0D

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

    def readSerialSerialQueue(self):
        while True :
            #print "try read from serial queue"
            dat = None
            time.sleep(3)
            try :
                dat = self.serialHandler.readItem()
                print "read S-queue->%s"%dat
            except Exception as inst :
                print ("read serial exception -> %s"%inst)
            if dat !=  None :
                print "read data -> %s"%dat
                if self.localNetStatus :

                    self.localPostQueue.put(dat)
                    print "put local queue->%d"%self.localPostQueue.qsize()
                if self.remoteNetStatus :
                    print "put remote queue->%d"%self.remotePostQueue.qsize()

                    self.remotePostQueue.put(dat)
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
            self.localPostHandler =  None
            self.localNetStatus =  False

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

    def readPostRemoteLoop(self):
        '''
        post add data to postHanderList[0]
        if wwwStatus == Ture ,just post to
        '''
        if not self.remoteNetStatus :
            print "remote net down"
            self.remotePostQueue.get()
            time.sleep(1)
        while True :
            if self.remotePostQueue.qsize() > 0 :
                buf = self.remotePostQueue.get()
                print "read from remote queue -> %s"%buf
                header =  buf[1:self.headerSize+1]
                content = buf[self.headerSize+1:-2]
                print len(buf),len(header),len(content),self.headerSize
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
            pass

    def parse_header(self,rawData):
        return None
    def parse_contend(self,rawData,cmdType):
        result = {"hello":1}
        return None
    def reset(self):
        self.cmdHeader = {}
        self.cmdBody = {}


