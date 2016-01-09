__author__ = 'dandan'
import json
import pprint


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
            if num == 0:
                pass
            else :
                pass
    def __toList(self,obj):
        pass
    def loadDict(self,dic):
        pass
    def getattribute(self,key):
        return self.__getattribute__(key)
    def sizeof(self):
        return 0
    def toJson(self):
        return json.dumps(self.toDict())
    def toRaw(self):
        return buffer(self)[:]

    def toHexRaw(self):
        return  self.toRaw()
    def loadRaw(self):
        pass
    def loadJson(self,js):
        pass
    def showCharArray(self):
        pass

    def getUint8(self,value):
        return "%2X"%value
    def getUint16(self,value):
        return "%s%s"%(self.getUint8(value>>8),self.getUint8(value & 0x00FF))
    def getUint32(self,value):
        return "%s%s"%(self.getUint16(value>>16),self.getUint16(value & 0x0000FFFF))
    def getUint64(self,value):
        return "%s%s"%(self.getUint16(value>>32),self.getUint16(value & 0x00000000FFFFFFFF))

class StructCmdHeader(StructBase):
    _define_ = [
        ("test2",4,2),
        ("test3",1,1),
        ("test4","StructBase",2),
    ]
if __name__ == "__main__" :
    test =  StructCmdHeader()
    test.test1 = 1
    test.test2 = 2
    test.test3 = 3
    print test.toDict()
    print test.getSize()
