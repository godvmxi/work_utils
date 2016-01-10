__author__ = 'dandan'
import  urllib2
import  urllib
import common_utils
import json
from common_utils import  HashUtils
from cmd_define import *

class HttpUtils():
    def __init__(self,hostname = None ,uri = None):
        self.posturi = "http://101.200.240.151/adminpanel/api.php"
        self.getUri = "http://101.200.240.151/adminpanel/get.php"
        self.delteUri = "http://101.200.240.151/adminpanel/delete.php"
    def __postData(self,dat):
        print dat
        # test_data_urlencode  = urllib.urlencode(dat)
        # print test_data_urlencode
        # print "post data"
        # print dat
        try :
            req = urllib2.Request(url = self.posturi,data =dat)
            res_data = urllib2.urlopen(req)
            res = res_data.read()
            # print type(res)
            # print  res_data
            return True
        except:
            return False
    def __getData(self,url):
        response  = urllib2.urlopen(url)

        # print response.info()
        #print response.geturl()
        if response.getcode() != 200:
            return None
        page = response.read()

        jsonDat = json.loads(page)
        body =  jsonDat["body"]
        httpSign =  jsonDat["sign"]
        oid =  None
        try :
            oid =  jsonDat["oid"]
        except :
            oid = None
        calSign  = HashUtils.calMd5hash(body)
        # print httpSign
        # print calSign
        result =  cmp(httpSign,calSign)


        if result == 0:
            return (body,oid)
        else :
            return None

    def check(self):
        response  = urllib2.urlopen(self.getUri)
        print response.getcode()
        # print response.info()
        print response.geturl()
        page = response.read()

        return False
    def post(self,cmdHeader,cmdData):
        cmdAll = {
            "header":cmdHeader,
            "content" : cmdData
        }
        rawStr =  json.dumps(cmdAll)
        sign =  HashUtils.calMd5hash(rawStr)
        jsonData = {
            "sign": sign,
            "body" : rawStr
        }

        print jsonData
        result   = self.__postData(json.dumps(jsonData) )
        print "+++++++++++++>",result
        return
    def get(self):
        return self.__getData(self.getUri)
    def deleteOid(self,oid):

        uri = "%s?oid=%s"%(self.delteUri,oid)
        print uri
        response  = urllib2.urlopen(uri)
        #print response.info()
        #print response.geturl()
        if response.getcode() != 200:
            return None
        page = response.read()
        return page
        #jsonDat = json.loads(page)


if __name__ == "__main__":
    getHandler = HttpUtils()
    postHandler =  HttpUtils()
    checkHandler = HttpUtils()

    # temp = getHandler.get()
    # print getHandler.deleteOid(temp[1])
    # print getHandler.check()
    # getHandler.post()
    cmdHeader = StructHeader()
    #
    # headerDict = cmdHeader.toDict()
    # rawStr =  json.dumps(headerDict)
    # cmdData=  {}
    # print rawStr
    # sign =  HashUtils.calMd5hash(rawStr)
    # jsonData = {
    #     "sign": sign,
    #     "body" : rawStr
    # }
    # print postHandler.post(headerDict,cmdData)
    result = getHandler.get()
    print result
    unicodestring = result[0]
    evalString =  eval(unicodestring)
    print type(evalString),evalString
    utf8string = unicodestring.encode("utf-8")
    print "utf8 -> ",utf8string
    evalString =  eval(utf8string)
    print type(evalString),evalString
    print json.loads(utf8string)
    # asciistring = unicodestring.encode("ascii")
    # print eval(asciistring)
    # print "ascii -> ",asciistring
    # print json.loads(asciistring)