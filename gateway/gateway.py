#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#import pack
import os
import time
import struct
from  ctypes import *
import ctypes
class Header(Structure) :
    _fields_ = [            ('cmdType',    ctypes.c_uint8) ,
                            ('hash',            ctypes.c_uint8) ,
                            ("length",          ctypes.c_uint8 ),
                            ('counter',       ctypes.c_uint16 ),
                            ('deviceId',      ctypes.c_uint16) ,
                            ('groupId',        ctypes.c_uint16)]
    def __str__(self):

        print self.cmdType
        print self.hash
        print self.length
        print self.counter
        return "{0}-{1}-{2}-{3}-{4}-{5}".format(  self.cmdType,  self.hash,  self.length,  self.hash,  self.hash,  self.hash)
    def dumpRaw(self):
        pass
    def loadRaw(self,raw):
        pass
def struct2stream(s):
    length = ctypes.sizeof(s)
    print length
    p       = ctypes.cast(ctypes.pointer(s), ctypes.POINTER(ctypes.c_char*length))
    return p.contents.raw

def stream2struct(string, stype):
    if not issubclass(stype, ctypes.Structure):
        raise ValueError('The type of the struct is not a ctypes.Structure')
    length      = ctypes.sizeof(stype)
    stream      = (ctypes.c_char * length)()
    stream.raw  = string
    p           = ctypes.cast(stream, ctypes.POINTER(stype))
    return p.contents
if __name__ == "__main__" :
    head = Header();
    head.cmdType=0x11
    head.hash=0xff
    print head
    raw = struct2stream(head)
    print repr(raw)
