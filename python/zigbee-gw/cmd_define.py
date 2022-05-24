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
            #print name,type ,num
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
                   # print class_name
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
        for name,valueType ,num in obj._define_ :
            # print "check- >",name,valueType,num
            if num == 1:
                if valueType in [0x01,0x02,0x04,0x08,0x11,0x12,0x14,0x18]:
                    result[name] = obj.__getattribute__(name)
                else :
                    value = obj.__getattribute__(name)
                    result[name] = value.toDict()
                pass
            elif num > 1 :
                if valueType in [0x01,0x02,0x04,0x08,0x11,0x12,0x14,0x18]:
                    value = []
                    #print obj.__getattribute__( name )
                    for i in range (0,num) :
                        value.append( obj.__getattribute__( name )[i]  )
                    result[name] = value
                else :
                    value = []
                    for i in range(0,num) :
                        value.append(obj.__getattribute__(name)[i].toDict())
                    result[name] = value
            else :
                raise Exception("wrong define number")
                pass
        self.size = self.getSize()
        return result

    def loadDict(self,dicData):
        if not isinstance(dicData,dict) :
            raise Exception("load value must be dict object")
        self.__loadDict(self,dicData)
        pass
    def __str__(self):
        return self.__class__.__name__
    def __loadDict(self,obj,dicValue):
        # print "++++++++++++++++++++++++"
        # print "handler class -> %s "%(obj._define_ )
        # print dicValue
        # print "items ???-> ",dicValue.keys()
        # print type(dicValue)
        for name,valueType ,num in obj._define_ :
            # print name,valueType ,num
            if num == 1:
                if valueType in [0x01,0x02,0x04,0x08,0x11,0x12,0x14,0x18]:

                    if dicValue.has_key(name) :
                        value  = dicValue[name]
                        setattr(obj,name ,value)
                    else :
                        # print "??????????"
                        raise Exception("dic has no target key item -> %s"%name)
                else :
                    if dicValue.has_key(name) :
                        # print "get sub dict"

                        subObj = getattr(obj,name)

                        value  = dicValue[name]

                        # print "load sub dict -> %s"%subObj
                        # print  "load dict -> %s"%value
                        subObj.loadDict(value)
                        # setattr(obj,name ,subObj)
                    else :
                        raise Exception("dic has no target key item -> %s"%name)
                pass
            elif num > 1 :
                if valueType in [0x01,0x02,0x04,0x08,0x11,0x12,0x14,0x18]:
                    subObjList = getattr(obj,name)


                    # print value
                    result = []
                    for i in range (0,num) :
                        hexStr = hexString[stringIndex:stringIndex+hexStrSize]
                        stringIndex = stringIndex + hexStrSize
                        listItem = self.hex2Bin(valueType,hexStr)
                        subObjList[i] = listItem
                else :
                    subObjList = getattr(obj,name)
                    hexStrSize = 2*(subObjList[1].getSize()  )
                    for i in range(0,num) :
                        hexStr = hexString[stringIndex:stringIndex+hexStrSize]
                        stringIndex = stringIndex + hexStrSize
                        subObjList[i].loadHex(hexStr)
            else :
                raise Exception("wrong define number")
        pass
    def sizeof(self):
        return  self.size
    def loadJson(self,jsonValue):
        dicValue = json.load(jsonValue)
        self.loadDict(dicValue)
    def toJson(self):
        return json.dumps(self.toDict())
    def toRaw(self):
        return None
    def toHex(self):
        return self.__toHex(self)
    def __toHex(self,obj):
        result = []
        for name,valueType ,num in obj._define_ :
            if num == 1:
                if valueType in [0x01,0x02,0x04,0x08,0x11,0x12,0x14,0x18]:
                    result.append(self.bin2Hex(valueType,getattr(obj,name)))
                else :
                    value = obj.__getattribute__(name)
                    result.append(value.toHex())
                pass
            elif num > 1 :
                if valueType in [0x01,0x02,0x04,0x08,0x11,0x12,0x14,0x18]:
                    # result.append("")
                    # print obj.__getattribute__( name )
                    value = getattr(obj,name)
                    # print value
                    for i in range (0,num) :
                        result.append( self.bin2Hex(valueType ,value[i]  ) )

                else :
                    value = getattr(obj,name)
                    for i in range(0,num) :
                        result.append(value[i].toHex())
            else :
                raise Exception("wrong define number")
                pass
        # print result
        return ''.join(result)

    def bin2Hex(self,valueType,value,littleEnd = False):
        if valueType in [0x01,0x11] :
            return  self.getUint8(value)
        elif valueType in [0x02,0x12] :
            return  self.getUint16(value)
        elif valueType in [0x04,0x14] :
            return  self.getUint32(value)
        elif valueType in [0x08,0x18] :
            return  self.getUint64(value)
        else :
            raise Exception("wrong data valueType")
    def hex2Bin(self,valueType,value):
        if valueType in [0x01,0x11] :
            return  int(value,16)
        elif valueType in [0x02,0x12] :
            value = "%s%s"%(value[2:4],value[0:2])
            return  int(value,16)
        elif valueType in [0x04,0x14] :
            value = "%s%s%s%s"%(value[6:8],value[4:6],value[2:4],value[0:2])
            return  int(value,16)
        elif valueType in [0x08,0x18] :
            value = "%s%s%s%s%s%s%s%s"%(value[14:16],value[12:14],value[10:12],value[8:10],value[6:8],value[4:6],value[2:4],value[0:2])
            return  int(value,16)
        else :
            raise Exception("wrong data valueType")
    def loadRaw(self):
        pass
    def loadHex(self,hexString):
        string_index = 0;
        if len(hexString) < self.size :
            raise Exception("%s-> the length can not short than the  double size"%self)
        self.__loadHex(self,hexString)

    def __loadHex(self,obj,hexString):
        stringIndex = 0
        for name,valueType ,num in obj._define_ :
            if num == 1:
                if valueType in [0x01,0x02,0x04,0x08,0x11,0x12,0x14,0x18]:
                    hexStrSize = 2*( ( valueType & 0x0F )  )
                    hexStr = hexString[stringIndex:stringIndex+hexStrSize]
                    stringIndex = stringIndex + hexStrSize

                    # subObj = getattr(obj,name)
                    temp = self.hex2Bin(valueType,hexStr)
                    setattr(obj,name ,temp)
                else :
                    subObj = getattr(obj,name)
                    hexStrSize = 2*(subObj.getSize()  )
                    # hexStrSize = 2*( value.getSize()  )
                    hexStr = hexString[stringIndex:stringIndex+hexStrSize]
                    stringIndex = stringIndex + hexStrSize

                    subObj = getattr(obj,name)
                    subObj.loadHex(hexStr)
                    # setattr(name ,value)
                pass
            elif num > 1 :
                if valueType in [0x01,0x02,0x04,0x08,0x11,0x12,0x14,0x18]:
                    subObjList = getattr(obj,name)
                    hexStrSize = 2*( ( valueType & 0x0F )  )

                    # print value
                    result = []
                    for i in range (0,num) :
                        hexStr = hexString[stringIndex:stringIndex+hexStrSize]
                        stringIndex = stringIndex + hexStrSize
                        listItem = self.hex2Bin(valueType,hexStr)
                        subObjList[i] = listItem
                else :
                    subObjList = getattr(obj,name)
                    hexStrSize = 2*(subObjList[1].getSize()  )
                    for i in range(0,num) :
                        hexStr = hexString[stringIndex:stringIndex+hexStrSize]
                        stringIndex = stringIndex + hexStrSize
                        subObjList[i].loadHex(hexStr)
            else :
                raise Exception("wrong define number")
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
    # def __str__(self):
    #     return self.__class__.__name__

''' test demo start'''''
class StructTimeTest(StructBase):
    _define_ =  [
       ("hour",1,1),
       ("minute",1,1),
       ("second",1,1),
       ("week",1,1),
    ]
class StructCmdHeaderTest(StructBase):
    _define_ = [
        ('cmdType',     1,              1 ),
        ('hash',        1,              1 ),
        ('length',      1,              1 ),
        ('counter',     1,              1 ),
        ('time',        'StructTimeTest',   1 ),
        ('srcGroupId',  1,              1 ),
        ('srcDeviceId', 1,              1 ),
        ('desGroupId',  1,              1 ),
        ('desDeviceId', 1,              1 ),
    ]
''' test demo end'''''
class StructPermission(StructBase):
    _define_ = [
        ('motion',     1,              1 ),
        ('lux',        1,              1 ),
        ('distance',      1,              1 ),
        ('reserved',     1,              1 ),
        ]
class StructTime(StructBase):
    _define_ =  [
       ("hour",1,1),
       ("minute",1,1),
       ("second",1,1),
       ("week",1,1),
    ]
class StructTriggerSource(StructBase):
    _define_ = [
        ('groupId',     1,              1 ),
        ('deviceId',    1,              1 ),
        ('fromType',    1,              1 ),
        ('fromOrder',   1,              1 ),
        ]
class  StructGroupPara(StructBase):
    _define_ = [
        ('groupId',     1,              1 ),
        ('deviceId',    1,              1 ),
        ('lampChannelBit',    1,              1 ),
        ('reserved',    1,              1 ),
        ]
class StructSwitchConfigPara(StructBase):
    _define_ = [
        ('luxOn',     2,              1 ),
        ('luxOff',    2,              1 ),
        ]
class StructLampCfg(StructBase):
    _define_ = [
        ('groupId',     1,              1 ),
        ('deviceId',    1,              1 ),
        ('curState',    1,              1 ),
        ('powerDefault',    1,              1 ),
        ]
# class StructTimeControlCfg(StructBase):
#     _define_ = [
#         ('week',     1,              1 ),
#         ('day',     1,              1 ),
#         ('hour',    1,              1 ),
#         ('min',     1,              1 ),
#         ]
class StructTimeControlCfg(StructBase):
    _define_ = [
        ('week',     1,              1 ),
        ('hour',     1,              1 ),
        ('hour',    1,              1 ),
        ('operation',     1,              1 ),
        ]
class StructNodeGroupCfg(StructBase):
    _define_ = [
        ('groupId',     1,              1 ),
        ('deviceId',    1,              1 ),
        ('lampChannelBit',    1,              1 ),
        ('reserved',    1,              1 ),
        ]
class StructHeader(StructBase):
    _define_ = [
        ('cmdType',     1,              1 ),
        ('hash',        1,              1 ),
        ('length',      2,              1 ),
        ('counter',     2,              1 ),
        # ('time',        'StructTime',   1 ),
        ("hour",        1,              1),
        ("minute",      1,              1),
        ("second",      1,              1),
        ("week",        1,              1),
        ('srcGroupId',  1,              1 ),
        ('srcDeviceId', 1,              1 ),
        ('desGroupId',  1,              1 ),
        ('desDeviceId', 1,              1 ),
    ]
class CmdSetupParaRequest(StructBase) :
    _define_ = [
        ('deviceType',     4,              1 ),
        ('ieee',           1,              8),
        ]
    pass
class CmdSetupParaSet(StructBase):
    _define_ = [
        ('deviceType',     4,              1 ),
        ('ieee',           1,              8 ),
        ('networkPanId',   2,              1 ),
        ('key',            1,              16 ),
    ]
    pass
class CmdActiveControllerSet(StructBase):
    _define_ = [
        # ('groupId',         1,              1 ),
        # ('deviceId',        1,              1 ),
        ('lightLevel',     1,              8 ),
        ('triggerSource',  "StructTriggerSource",1 )
    ]
    pass
class CmdActionCollect(StructBase): #no need now
    _define_ = [
        ('groupId',         1,              1 ),
        ('deviceId',        1,              1 )]

class CmdWorkingParaRequest(StructBase):
    _define_ = [
        ('DeviceType',     1,              1 ),
        ('ieee',        1,              8 )]

class CmdControllerParaSet(StructBase):
    _define_ = [
        ('groupId',     1,              1 ),
        ('deviceId',     1,              1 ),
        ('deviceType',     4,              1 ),
        ('permission',     4,              1 ),
        ('groupNum',     2,              1 ),
        ('groupParaList',     1,              1 ),
        ]

class CmdSwitchParaSet(StructBase):
    _define_ = [
        ('groupId',     1,              1 ),
        ('deviceId',    1,              1 ),
        ('lightModify',   2,              1 ),
        ('deviceType',    4,              1 ),
        ('lampConfig',    'StructLampCfg',1),
        ('permission',    'StructPermission',              1 ),
        ('reportInterval',        2,              1 ),
        ('timeControlParaNum',    2,              1 ),
        ('timeControlPara',    "StructTimeControlCfg",              8 ),
        ('switchConfigPara',    'StructSwitchConfigPara',              1 ),
        ]
    pass
class CmdSyncTimeSet(StructBase):
    _define_ = [
        ('week',     1,              1 ),
        ('hour',     1,              1 ),
        ('minute',     1,              1 ),
        ('second',        1,              1 )]
    pass
class CmdPermissionPara(StructBase):
    _define_ = [
        ('groupId',     1,              1 ),
        ('deviceId',     1,              1 ),
        ('deviceType',     4,              1 ),
        ('permission',        'StructPermission',   1 ),
        ('timeout',    16 ,              1 )
        ]
class CmdPermissionSet(StructBase):
    _define_ = [
        ('cmdType',     1,              1 ),
        ('hash',        1,              1 )]
    pass
class CmdForceNodeRegist(StructBase):
    _define_ = [
        ('cmdType',     1,              1 ),
        ('hash',        1,              1 )]
    pass
class CmdSwitchState(StructBase):
    _define_ = [
        ('cmdType',     1,              1 ),
        ('hash',        1,              1 )]
    pass
class CmdControllerState(StructBase):
    _define_ = [
        ('cmdType',     1,              1 ),
        ('hash',        1,              1 )]


class CmdTypeUtils():
    cmd_setup_para_requset          = 0x01
    cmd_setup_para_set              = 0x02
    cmd_active_controller_set       = 0x04
    cmd_action_collect              = 0x05
    cmd_working_para_request        = 0x06
    cmd_controller_para_set         = 0x07
    cmd_switch_papa_set             = 0x08
    cmd_sync_time_set               = 0x09
    cmd_permisson_set               = 0x0A
    cmd_force_node_regist           = 0x0B
    cmd_switch_state                = 0x0C
    cmd_controller_state            = 0x0D
    def __init__(self):
        pass
    def getCmdDataObject(self,cmdType):
        className = None
        if cmdType == self.cmd_setup_para_requset:
            self.className = "CmdSetupParaRequest"
        elif cmdType ==  self.cmd_setup_para_set :
            self.className = "CmdSetupParaSet"
        elif cmdType ==  self.cmd_active_controller_set :
            self.className = "CmdActiveControllerSet"
        elif cmdType ==  self.cmd_action_collect :
            self.className = "CmdActionCollect"
        elif cmdType ==  self.cmd_working_para_request :
            self.className = "CmdWorkingParaRequest"
        elif cmdType ==  self.cmd_controller_para_set :
            self.className = "CmdControllerParaSet"
        elif cmdType ==  self.cmd_switch_papa_set :
            self.className = "CmdSwitchParaSet"
        elif cmdType ==  self.cmd_sync_time_set :
            self.className = "CmdSyncTimeSet"
        elif cmdType ==  self.cmd_permisson_set :
            self.className = "CmdPermissionSet"
        elif cmdType ==  self.cmd_force_node_regist :
            self.className = "CmdForceNodeRegist"
        elif cmdType ==  self.cmd_switch_state :
            self.className = "CmdSwitchState"
        elif cmdType ==  self.cmd_controller_state :
            self.className = "CmdControllerState"
        else:
            self.className = None
            pass

        if self.className == None :
            return None
        else :
            self.className = "%s()"%self.className
            return eval(self.className)
    def getCurClassName(self):
        return self.className


if __name__ == "__main__" :
    header =  StructCmdHeaderTest()
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
    print  "----------------dump hex-----------------------------"
    dictValue =  header.toDict()
    print dictValue
    print header.getSize()
    hexString =  header.toHex()
    print hexString
    print  "----------------load hex and dump check-----------------------------"

    loadHexHeader =  StructCmdHeaderTest()
    loadHexHeader.loadHex(hexString)
    print loadHexHeader.toDict()
    print loadHexHeader.getSize()
    print loadHexHeader.toHex()

    print "----------------load dict and dump check-----------------------------"
    loadDictHeader =  StructCmdHeaderTest()
    loadDictHeader.loadDict(dictValue)
    print loadDictHeader.toDict()
    print loadDictHeader.getSize()
    print loadDictHeader.toHex()
    header = StructHeader()
    headerDict = header.toDict()
    setupParaSet = CmdSetupParaSet()
    bodyDict =  setupParaSet.toDict()
    print setupParaSet.toJson()
    cmd = {
            "header":headerDict,
            "content":bodyDict
    }

    body = {
        "body":json.dumps(cmd),
        "sign":"dsfasdf",
        "oid" : 123

    }
    print json.dumps(body)


    setupParaSet = CmdControllerParaSet()
    bodyDict =  setupParaSet.toDict()
    print setupParaSet.toJson()
    cmd = {
            "header":headerDict,
            "content":bodyDict
    }

    body = {
        "body":json.dumps(cmd),
        "sign":"dsfasdf",
        "oid" : 123

    }
    print json.dumps(body)

    setupParaSet =  CmdSwitchParaSet()
    bodyDict =  setupParaSet.toDict()
    print setupParaSet.toJson()
    cmd = {
            "header":headerDict,
            "content":bodyDict
    }

    body = {
        "body":json.dumps(cmd),
        "sign":"dsfasdf",
        "oid" : 123

    }
    print json.dumps(body)



