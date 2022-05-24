__author__ = 'Bright Jiang'
from  ctypes import *
class StructBase():
    _fields_ = [            ('cmdType',    ctypes.c_uint8) ,
                            ('hash',            ctypes.c_uint8) ,
                            ("length",          ctypes.c_uint8 ),
                            ('counter',       ctypes.c_uint16 ),
                            ('deviceId',      ctypes.c_uint16) ,
                            ('groupId',        ctypes.c_uint16)]
    def  __str__(self):
        pass
    def toJson(self):
        pass

if __name__ == "__main__" :
    test = StructBase()
    test.toJson()
    pass