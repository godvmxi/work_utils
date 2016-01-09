__author__ = 'Bright Jiang'
from  ctypes import *
import ctypes
import json
import pprint
def hexShow(raw):
    rawLen = len(raw)
    print "raw-> %d "%rawLen
    for index in range(0,rawLen) :
        print ("%2x "%int(raw[index] ,10)),
    print


class StructBasicBase(Structure):
    _fields_ = [            ('basic1',    ctypes.c_uint16) ,
                            ('basic2',    ctypes.c_uint16) ]
    def toDict(self):
        result = {}
        for field in self._fields_ :
            key = field[0]
            result[key] = self.getattribute(key)
        return result
    def loadDict(self,dic):
        pass
    def getattribute(self,key):
        return self.__getattribute__(key)
    def sizeof(self):
        return ctypes.sizeof(self)
    def toJson(self):
        return json.dumps(self.toDict())
    def toRaw(self):
        return buffer(self)[:]
        length = ctypes.sizeof(self)
        #print length
        p       = ctypes.cast(ctypes.pointer(self), ctypes.POINTER(ctypes.c_char*length ) )
        # print p
        # print str(p.contents.raw)
        return p.contents.raw

    def toHexRaw(self):
        return  self.toRaw()
    def loadRaw(self):
        pass
    def loadJson(self,js):
        pass
    def showCharArray(self):
        pass





class StrucAdvanceBase(StructBasicBase):
    _fields_ = [
                    ('advance1',    ctypes.c_uint32*2),
                    ('advance2',    ctypes.c_uint32),
                    ('subClass',      (StructBasicBase*3) )  ]

    def toDict(self):
        result = {}
        for field in self._fields_ :
            key = field[0]
            result[key] = self.getattribute(key)
        return result
    def isBasicCtype(self,value):
        basic_types = (ctypes.c_short, ctypes.c_int, ctypes.c_long, ctypes.c_longlong ,
                       ctypes.c_ushort, ctypes.c_uint, ctypes.c_ulong, ctypes.c_ulonglong,
                       ctypes.c_uint8,ctypes.c_uint16,ctypes.c_uint32
        )
        # if type(value) in basic_types:
        #     return True
        # else :
        #     return False
        return  isinstance(value,basic_types)

        return True
    def getattribute(self,key):
        value = self.__getattribute__(key)
        # print issubclass( value ,ctypes.c_uint8)
        print "??key -> %s :%s"%(key,type(value))
        if  isinstance(value,StructBasicBase):
            print "class type -> %s :%s"%(key,type(value))
            return value.toDict()
        elif  isinstance(value ,ctypes.Array):
            print "array type -> %s :%s"%(key,type(value))
            result = []
            for item in value :
                pass
            return
        else :
            print "basic type -> %s :%s"%(key,type(value))
            return value

    def toJson(self):
        return json.dumps(self.toDict() )
    def  __str__(self):
        pass


def struct2stream(s):
    length = ctypes.sizeof(s)
    #print length
    p       = ctypes.cast(ctypes.pointer(s), ctypes.POINTER(ctypes.c_char*length ) )
    return p.contents.raw

def stream2struct(string, stype):
    if not issubclass(stype, ctypes.Structure):
        raise ValueError('The type of the struct is not a ctypes.Structure')
    length      = ctypes.sizeof(stype)
    stream      = (ctypes.c_char * length)()
    stream.raw  = string
    p           = ctypes.cast(stream, ctypes.POINTER(stype))
    return p.contents
class CmdTime(StructBasicBase):
    _fields_ = [
                    ('hour',     ctypes.c_uint8),
                    ('minute',     ctypes.c_uint8),
                    ('second',     ctypes.c_uint8)
                ]
class CmdHeader(StructBasicBase):

    _fields_ = [
                    ('cmdType',    ctypes.c_uint8),
                    ('hash',    ctypes.c_uint8),
                    ('length',     ctypes.c_uint16),
                    ('counter',     ctypes.c_uint8),
                    # ('time',CmdTime),
                    ('timeHour',     ctypes.c_uint8),
                    ('timeMinute',     ctypes.c_uint8),
                    ('timeSecond',     ctypes.c_uint8),
                    ('srcGroupId',     ctypes.c_uint16),
                    ('srcDeviceId',     ctypes.c_uint16),
                    ('desDeviceId',     ctypes.c_uint16),
                    ('desDeviceId',     ctypes.c_uint16),
                    ]


class CmdNodeSetupRequest(StructBasicBase):
    _fields_ = [
                    ('deviceType',    ctypes.c_uint32),
                    ('ieee',         ctypes.c_uint64)
                    ]


if __name__ == "__main__" :
    cmdHeader = CmdHeader()
    cmdHeader.cmdType = 0x01
    cmdHeader.hash = 0x02
    cmdHeader.length = 0x03
    cmdHeader.counter =  0x04
    # cmdHeader.time.hour = 0x05
    # cmdHeader.time.minute = 0x06
    # cmdHeader.time.second = 0x07
    cmdHeader.srcGroupId= 0x08
    cmdHeader.srcDeviceId = 0x09
    cmdHeader.desGroupId= 0x0A
    cmdHeader.desDeviceId = 0x0B


    print cmdHeader.toDict()
    stream =  struct2stream(cmdHeader)
    print "stream len-> ",len(stream)
    print repr(stream)
    stream  = cmdHeader.toHexRaw()
    print "stream len-> ",len(stream)
    print repr(stream)


    exit()
    basic = StructBasicBase()
    basic.basic1 = (0xFFEE)
    basic.basic2 = (0xDDCC)
    print basic.toDict()
    print "basic size-> %d"%( basic.sizeof() )
    print "basic to steam"
    stream = struct2stream(basic)
    #print stream
    print repr(stream)
    # exit()
    advance = StrucAdvanceBase()
    advance.advance1[0] = 0xEDDCCBBA
    advance.advance2 = 0xEEDDCCBB
    advance.subClass[0].basic1 = 0xFFEE
    advance.subClass[0].basic2 = 0xDDCC
    advance.subClass[1].basic1 = 0xEEFF
    advance.subClass[1].basic2 = 0xCCDD
    print "advance size ->%d"%advance.sizeof()
    pprint.pprint(  advance.toDict() )
    print "advence to steam"
    stream =   struct2stream(advance)
    print repr(stream)
    print repr(stream[4:])

    #print test.toJson()
