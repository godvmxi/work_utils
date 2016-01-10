__author__ = 'dandan'
import  urllib2
import  urllib
import common_utils
import json
from common_utils import  HashUtils

class HttpUtils():
    def __init__(self,hostname = None ,uri = None):
        self.posturi = "http://101.200.240.151/adminpanel/api.php"
        self.getUri = "http://101.200.240.151/adminpanel/get.php"
        self.delteUri = "http://101.200.240.151/adminpanel/delete.php"
    def __postData(self,dat):
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
    def post(self,jsonData):
        self.__postData(jsonData)

        pass
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
        jsonDat = json.loads(page)


if __name__ == "__main__":
    getHandler = HttpUtils()
    postHandler =  HttpUtils()
    checkHandler = HttpUtils()

    temp = getHandler.get()
    print getHandler.deleteOid(temp[1])
    print getHandler.check()
    # getHandler.post()
