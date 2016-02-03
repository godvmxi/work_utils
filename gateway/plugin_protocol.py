#!/usr/bin/env python2.7
# -*- coding:utf-8 -*-
__author__ = 'dandan'
import json
import socket
import fcntl
import struct
def protocalLogin( loid = "",mac= '',token=""):
    result = {
        "RPCMethod" : "Boot" ,
        "LOID" : loid,
        "MAC" : mac ,
        "Token" :token
    }
    return json.dumps(result)
    pass
def protocolLoinout():
    pass
def getIfaceIpAddr(iface):
    return ""
def protocolConnectDistributionPlatform(token= ""):
    result = {
        "RPCMethod" : "BootFirst" ,
        "Vendor" :'' "",
        "Model" : "" ,
        "Token" :token ,
        "FirmwareVer":"",
        "HardwareVer":"",
        "MAC" : "" ,
        "IPAddr" :"",
        "PlatformID" :"other"
    }
    return json.dumps(result)
class HoseInfoUtils():
    def __init__(self):
        pass
    def __getMac(self):
        pass
    def __getVendor(self):
        pass
    def __getModel(self):
        pass
    def __getHwVer(self):
        self.hwVer = "1.0"
    def __getSwVer(self):
        self.swVer = "2.0.0"
        pass
    def __getPlatFormId(self):
        self.platFormId = "1111"
        pass

    staticmethod
    def getHostIpMac(cls,ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', ifname[:15]))
        print info


class  ProtocolUtils():
    def __init__(self):
        pass

    def __getToken(self):
        self.token  = ""
        return self.token
if __name__ == "__main__" :
    result =  protocalLogin("loid","123456789012","fdsfasfdaasd")
    print result
    result =  protocolConnectDistributionPlatform()
    print result
    HoseInfoUtils.getHostIpMac("本地连接")