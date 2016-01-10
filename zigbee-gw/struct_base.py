__author__ = 'dandan'
import json
import pprint
import binascii

class StructBase(object):
    '''
    _define_ :define  struct , size of value by byte ,
            unsign type :0x01,0x02,0x04 ,0x08
            sign type :0x11,,0x12,0x14.0x18
            class : 0 ,class is inherited from me
            not use ctype structure ,it's type and Nested structure make crazy
    '''
    _define_ = [
        ("test1",4,1),# (name,sizeof,num)

    ]
    def __init__(self):
        '''
        init object data,just reset to 0
        '''
        self.keys = []
        self.size = 0  #please align your struct
        for name,type ,num in self._define_ :
            print name,type ,num
            self.keys.append(name)
            if num  ==  1 :
                if type in [0x01,0x02,0x04,0x08,0x11,0x12,0x14,0x18]:
                    self.__setattr__(name,0)
                else :
                    class_name = "%s()"%type
                    self.__setattr__(name,eval(class_name))
            elif num > 1 :
                value = []
                if type in [0x01,0x02,0x04,0x08,0x11,0x12,0x14,0x18]:
                    for i in range(0,num):
                        value.append(0)
                    self.__setattr__(name,value)
                else :
                    class_name = "%s()"%type
                    print class_name
                    for i in range(0,num):
                        value.append(eval(class_name))
                    self.__setattr__(name,value)
            else :
                raise Exception("wrong object number")
            if type in [0x01,0x02,0x04,0x08,0x11,0x12,0x14,0x18]:
                self.size = self.size + (type&0x0F)*num
            else :
                if num == 1 :
                    self.size = self.size + self.__getattribute__(name).getSize()
                else :
                    self.size = self.size + self.__getattribute__(name)[0].getSize()*num
    def getSize(self):
        return self.size
    def __str__(self):
        pass
    def toDict(self):
        return self.__toDict(self)
    def __toDict(self,obj):
        result = {}
        for name,type ,num in obj._define_ :
            print "check- >",name,type,num
            if num == 1:
                if type in [0x01,0x02,0x04,0x08,0x11,0x12,0x14,0x18]:
                    result[name] = obj.__getattribute__(name)
                else :
                    value = obj.__getattribute__(name)
                    result[name] = value.toDict()
                pass
            elif num > 1 :
                if type in [0x01,0x02,0x04,0x08,0x11,0x12,0x14,0x18]:
                    value = []
                    print obj.__getattribute__( name )
                    for i in range (0,num) :
                        value.append( obj.__getattribute__( name )[i]  )
                    result[name] = value
                else :
                    value = []
                    for i in range(0,num) :
                        value.append(obj.__getattribute__(name)[i].toDict())
                    result[name] = value
            else :
                print "dsfasdafsd"
                pass

        return result

    def loadDict(self,dic):
        pass

    def sizeof(self):
        return  self.size
    def toJson(self):
        return json.dumps(self.toDict())
    def toRaw(self):
        return buffer(self)[:]
    def toHex(self):
        return self.__toHex(self)
    def __toHex(self,obj):
        result = []
        for name,type ,num in obj._define_ :
            if num == 1:
                if type in [0x01,0x02,0x04,0x08,0x11,0x12,0x14,0x18]:
                    result.append(self.getHexFromType(type,getattr(obj,name)))
                else :
                    value = obj.__getattribute__(name)
                    result.append(value.toHex())
                pass
            elif num > 1 :
                if type in [0x01,0x02,0x04,0x08,0x11,0x12,0x14,0x18]:
                    # result.append("")
                    # print obj.__getattribute__( name )
                    value = getattr(obj,name)
                    # print value
                    for i in range (0,num) :
                        result.append( self.getHexFromType(type ,value[i]  ) )

                else :

                    for i in range(0,num) :
                        result.append(obj.__getattribute__(name)[i].toHex())
            else :
                raise Exception("wrong define number")
                pass
        print result
        return ''.join(result)
    def loadHex(self,hex):
        pass
    def getHexFromType(self,type,value):
        if type in [0x01,0x11] :
            return  self.getUint8(value)
        elif type in [0x02,0x12] :
            return  self.getUint16(value)
        elif type in [0x04,0x14] :
            return  self.getUint32(value)
        elif type in [0x08,0x18] :
            return  self.getUint64(value)
        else :
            raise Exception("wrong data type")
    def loadRaw(self):
        pass
    def loadJson(self,js):
        pass
    def showCharArray(self):
        pass

    def getUint8(self,value):
        #return binascii.hexlify(value)
        result = "%2X"%value
        if result[0] == ' ':
             result = '0'+result[1]
        return result
    def getUint16(self,value):
        return "%s%s"%(self.getUint8(value>>8),self.getUint8(value & 0x00FF))
    def getUint32(self,value):
        return "%s%s"%(self.getUint16(value>>16),self.getUint16(value & 0x0000FFFF))
    def getUint64(self,value):
        return "%s%s"%(self.getUint16(value>>32),self.getUint16(value & 0x00000000FFFFFFFF))
class StructTime(StructBase):
    _define_ =  [
       ("hour",1,1),
       ("minute",1,1),
       ("second",1,1)
    ]
class StructCmdHeader(StructBase):
    _define_ = [
        ('cmdType',     1,              1 ),
        ('hash',        1,              1 ),
        ('length',      2,              1 ),
        ('counter',     1,              1 ),
        ('time',        'StructTime',   1 ),
        ('srcGroupId',  2,              1 ),
        ('srcDeviceId', 2,              1 ),
        ('desDeviceId', 2,              1 ),
        ('desDeviceId', 2,              1 ),
    ]
if __name__ == "__main__" :
    header =  StructCmdHeader()
    header.cmdType = 1
    header.hash  = 0x02
    header.length = 0x0304
    header.counter =  0x05
    header.time.hour = 0x06
    header.time.minute = 0x07
    header.time.second = 0x08
    header.srcGroupId = 0x090A
    header.srcDeviceId = 0x0B0C
    header.desGroupId = 0x090A
    header.desDeviceId = 0x0B0C
    print header.toDict()
    print header.getSize()
    print header.toHex()
