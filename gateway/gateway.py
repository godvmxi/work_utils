#!/usr/bin/env python2.7
#import pack
import os
import time
import struct
from  ctypes import *
import ctypes
class Header(Structure) :
    _field_ = [ ('cmdType',    c_ubyte) ,
                            ('hash',            c_ubyte) ,
                            ('test',          c_ubyte ),
                            ('counter',       ctypes.c_uint16 ),
                            ('deviceId',      ctypes.c_uint16) ,
                            ('groupId',        ctypes.c_uint16)]
    def __str__(self):

        print self.cmdType
        print self.hash
        print self.test
        print self.counter
        return "{0}-{1}-{2}-{3}-{4}-{5}".format(  self.cmdType,  self.hash,  self.len,  self.hash,  self.hash,  self.hash)
    
if __name__ == "__main__" :
    head = Header();
    head.cmdType=0x11
    head.hash=0xff
    print head