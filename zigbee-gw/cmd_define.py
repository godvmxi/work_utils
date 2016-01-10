#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import json
import sys
from optparse import OptionParser 
import time
import hashlib
import urllib
import urllib2
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
class HashUtils():
    salt = "660235c0d59758ccc33d9c969d8c1643"
    def __init__(self):
        pass
    @classmethod
    def calMd5hash(cls,str):
        m = hashlib.md5()
        md5_str = "%s%s"%(str,cls.salt)
        m.update(md5_str)
        return m.hexdigest()

class CmdStructUtils():
    cmd_node_setup_requset = 0x01
    cmd_node_setup_para_set = 0x02
    cmd_active_controller_set =  0x04
    cmd_action_collect = 0x05
    cmd_node_working_para_request  =  0x06
    cmd_controller_para_set = 0x07
    cmd_switch_papa_set = 0x08
    cmd_server_check_time = 0x09
    cmd_node_permisson_set = 0x0A
    cmd_force_node_regist  = 0x0B
    cmd_switch_state   = 0x0C
    cmd_controller_state = 0x0D
    
    def __init__(self):
        self.sign={"sign":"sign string"}
        self.header =  { "cmdType":0,
                "hash":0,
                "lenght":0,
                "counter" : 0,
                "time" : None,
                "deviceId" : 0,
                "groupId":0
                }
        self.content = {
                
        }
        self.request = {"sign":self.sign}
        self.salt = "660235c0d59758ccc33d9c969d8c1643"
        pass
    def genHeader(self,cmdType):
        self.header["cmdType"] = cmdType
        self.header["time"] = time.ctime()
        pass
    
        
    def getHeaderJson(self):
        return json.dumps(self.header)
        pass
    def getContentJson(self):
        return json.dumps(self.content)
        pass
    def setAuth(self,user="admin",password="admin",salt = "660235c0d59758ccc33d9c969d8c1643"):
        self.user =  user
        self.password = password
        self.salt =  salt
    def HeaderType(self):
        pass
    def genDataBody(self):
        self.body  = {
                    "header":self.header,
                    "content":self.content
                }
        self.body =  json.dumps(self.body)
        pass
    def getRequestJson(self):
        self.genDataBody()
        self.request={  "sign":HashUtils.calMd5hash(self.body),
                        "body":self.body
                        }
        #return self.request'
        # return self.request
        return json.dumps(self.request)
        return json.dumps(self.request,sort_keys=True,indent=4)

    def reInit(self):
        pass
    def loadCmdJson(self):
        pass
    def getCmdJson(self):
        pass
    def setHeader(self,hash=0xff,deviceId=0,cmdType=1,Length=255,counter=0,groupId=0):
        self.header = { "cmdType":0x01,
            "hash":0xff,
            "lenght":0xff,
            "counter" : 0,
            "time" : None,
            "deviceId" : 0x00,
            "groupId":0x01,
        }
        self.header['cmdType'] = type
        self.header["Time"] = time.ctime()
        return self.header
    def calMd5hash(self,str):
        m = hashlib.md5()
        md5_str = "%s%s"%(str,self.salt)
        m.update(md5_str)
        return m.hexdigest()
        
    def genDemoSetupPara(self):
        self.genHeader(self.cmd_node_setup_para_set)
        self.content = {
            "ieee" :"0123456789ABCDEF",
            "deviceType":0x1,
            "deviceMode":0x02,
            "networkPadId":0xDDDD,
            "key":"salt",#use  this salt to cal working network sha128 key
        }
        self.request = {
                
                "header" :self.header,
                "content":self.content
                }
        return json.dumps(self.request)
    def genDemoAck(self):
        self.genHeader(self.cmd_node_setup_para_set)
        self.content = {
            "ieee" :"0123456789ABCDEF",
            "deviceType":0x1,
            "deviceMode":0x02,
            "networkPadId":0xDDDD,
            "key":"salt",#use  this salt to cal working network sha128 key
        }
        self.request = {
                
                "header" :self.header,
                "content":None
                }
        return json.dumps(self.request)
    def genDemoSetupRequest(self):
        self.genHeader(self.cmd_node_setup_requset)
        self.content = {
            "ieee" :"0123456789ABCDEF",
            "deviceType":11
        }
        self.request = {
                
                "header" :self.header,
                "content":self.content
                }
        return json.dumps(self.request)
    def genDemoNodeActiveControl(self):
        self.genHeader(self.cmd_active_controller_set)
        self.content = {
            "groupId":3,
            "deviceId":2,
            "lightLevel" :1 ,
            'permisson':0xFFEEDDAA
        }
        self.request = {
                
                "header" :self.header,
                "content":self.content
                }
        return json.dumps(self.request)
        pass
    def genDemoActionCollect(self):
        self.genHeader(self.cmd_action_collect)
        self.content = {
            "groupId":3,
            "deviceId":2,
            "TriggerSource" :0xDDDDDDDD,
            'TriggerFrom':0xFFEE,
            'TriggerToGroup':0xBBBB,
            'TriggerToDevice':0xAAAA,
            'TriggerOrder':0xFEDA,
        }
        self.request = {
                
                "header" :self.header,
                "content":self.content
                }
        return json.dumps(self.request)
    def genDemoWorkingParaRequest(self): #repay according the node type
        self.genHeader(self.cmd_node_setup_requset)
        self.content = {
            "note":"just replay according to the node type",
        }
        self.request = {
                
                "header" :self.header,
                "content":self.content
                }
        return json.dumps(self.request)
    
    def genDemoSwitchWorkingParaSet(self):
        self.genHeader(self.cmd_switch_papa_set)
        self.content = {
            "groupId":0x1234,
            "deviceId":0x5678,
            "deviceType":2,
            "Permission":0x01010101,
            "LightFix" : 0,
            "permisson":0x01010101,
            "ReportInterval": 0 ,
            "TimeControlParaNum":7,
            "TimeControlPara":[ 
                        {'WeekDay':0x2,"WorkTIme":0x2,"Operation":""},  
                        {'WeekDay':0x2,"WorkTIme":0x2,"Operation":""},  
                        {'WeekDay':0x2,"WorkTIme":0x2,"Operation":""},  
                        {'WeekDay':0x2,"WorkTIme":0x2,"Operation":""},  
                        {'WeekDay':0x2,"WorkTIme":0x2,"Operation":""},  
                        {'WeekDay':0x2,"WorkTIme":0x2,"Operation":""},  
                        {'WeekDay':0x2,"WorkTIme":0x2,"Operation":""}
                        
                        ]
            }

        self.request = {
                
                "header" :self.header,
                "content":self.content
                }
        return json.dumps(self.request)
        return json.dumps(self.request,sort_keys=True,indent=2)
    def genDemoControllerWorkingParaSet(self):
        self.genHeader(self.cmd_controller_para_set)
        self.content = {
            "deviceType":2,
            "Permission":0x01010101,
            "LightFix" : 0,
            "permisson":0x01010101,
            "LampNumber":2,
            "LightController":[
                {"groupId":0x1,"deviceId":2,"CurrentState":0},
                {"groupId":0x1,"deviceId":2,"CurrentState":0},
                {"groupId":0x1,"deviceId":2,"CurrentState":0},
            {"groupId":0x1},

            ],#
            "TimeControlParaNum":0,
            "TimeControlPara":[]
            
        }
        self.request = {
                
                "header" :self.header,
                "content":self.content
                }
        return json.dumps(self.request)
    def genDemoCheckTime(self):
        self.genHeader(self.cmd_server_check_time)
        self.content = {
            "week":7,
            "hour":2,
            "min":12,
            "second":12
        }
        self.request = {
                
                "header" :self.header,
                "content":self.content
                }
        return json.dumps(self.request,sort_keys=True,indent=2)
    def genDemoNodepermissonSet(self):
        self.genHeader(self.cmd_node_permisson_set)
        self.content = {
            "permisson":0x01010101
        }
        self.request = {
                
                "header" :self.header,
                "content":self.content
                }
        return json.dumps(self.request,sort_keys=True,indent=2)
    
    def genDemoNodeForceRegist(self):
        self.genHeader(self.cmd_force_node_regist)
        self.content = {
            "ieee":"0x01234567890"
        }
        self.request = {
                
                "header" :self.header,
                "content":self.content
                }
        return json.dumps(self.request,sort_keys=True,indent=2)
    




class HttpUtils():
    def __init__(self):
        self.posturi = "http://101.200.240.151/adminpanel/api.php"
        self.getUri = "http://101.200.240.151/adminpanel/get.php"
        
        pass
    def postData(self,dat):
        print dat
        # test_data_urlencode  = urllib.urlencode(dat)
        # print test_data_urlencode
        print "post data"
        print dat
        req = urllib2.Request(url = self.posturi,data =dat)

        res_data = urllib2.urlopen(req)

        print "return ->"
        res = res_data.read()

        print res
    def getData(self):
        response  = urllib2.urlopen(self.getUri)
        print response.getcode()
        # print response.info()
        print response.geturl()
        page = response.read()
        jsonDat = json.loads(page)
        print "try ->"
        body =  jsonDat["body"]
        sign =  jsonDat["sign"]
        print body
        print sign
        calSign  = HashUtils.calMd5hash(body)
        print calSign
        print ""



        print page

    
if __name__ == "__main__" :

    parser = OptionParser() 
    parser.add_option("-c", "--cmdType", action="store_true", 
                    dest="cmdType", 
                    default=None, 
                    help="cmd type") 
    parser.add_option("-t", "--requsetType", action="store_true", 
                    dest="requsetType", 
                    default='get', 
                    help="http request type,just support get & post") 
    parser.add_option("-s", "--server", action="store_true", 
                    dest="server", 
                    default='http://127.0.0.1', 
                    help="http host name")   
                    
                               
    (options, args) = parser.parse_args() 
    
    
    restTool = HttpUtils()
    requestData =CmdStructUtils()
    # print "genDemoSetupPara"
    # requestData.genDemoSetupPara()
    # print requestData.getRequestJson()
    # print
    # print "genDemoSetupRequest"
    # print requestData.genDemoSetupRequest()
    # print requestData.getRequestJson()
    #
    # print "genDemoAck"
    # print requestData.genDemoAck()
    # print requestData.getRequestJson()
    #
    # print "genDemoNodeActiveControl"
    # print requestData.genDemoNodeActiveControl()
    # print requestData.getRequestJson()
    #
    # print "genDemoActionCollect"
    # print requestData.genDemoActionCollect()
    # print requestData.getRequestJson()
    #
    # print "genDemoWorkingParaRequest"
    # print requestData.genDemoWorkingParaRequest()
    # print requestData.getRequestJson()
    #
    # print "genDemoSwitchWorkingParaSet"
    # print requestData.genDemoSwitchWorkingParaSet()
    # print requestData.getRequestJson()
    #
    # print "genDemoControllerWorkingParaSet"
    # print requestData.genDemoControllerWorkingParaSet()
    # print requestData.getRequestJson()
    #
    # print "genDemoCheckTime"
    # print requestData.genDemoCheckTime()
    # print requestData.getRequestJson()
    #
    # print "genDemoNodepermissonSet"
    # print requestData.genDemoNodepermissonSet()
    # print requestData.getRequestJson()
    
    # print "genDemoNodeForceRegist"
    # print requestData.genDemoNodeForceRegist()
    # test =  requestData.getRequestJson()
    # print test
    # print type(test)



    # restTool.postData(test)

    # print "genDemoNodeActiveControl"
    # print requestData.genDemoNodeActiveControl()
    # test  = requestData.getRequestJson()

    print "genDemoSetupRequest"
    requestData.genDemoSetupRequest()
    test =  requestData.getRequestJson()

    #
    # print "genDemoSetupRequest"
    # print requestData.genDemoSetupRequest()
    # test = requestData.getRequestJson()



    restTool.postData(test)
    # restTool.getData()
    

