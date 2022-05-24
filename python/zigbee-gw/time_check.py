#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
__author__ = 'Bright Jiang'
import os
import  time
import time
import os
import httplib
from optparse import OptionParser
class CheckTime():
    rtc_reg_control_1   = 0
    rtc_reg_control_2   = 1
    rtc_reg_second      = 2
    rtc_reg_minute      = 3
    rtc_reg_hour        = 4
    rtc_reg_day         = 5
    rtc_reg_week        = 6
    rtc_reg_month       = 7
    rtc_reg_year        = 8

    def __init__(self):
        self.rtc_bcd_time = {}
        self.sys_time = ''
        self.rtc_get_time_cmd = 'i2cdump  -y -f -r 0-15 0 0x51 b'
        self.rtc_raw_time  =None
        self.rtc_bin_time ={}

    def bcd2hex(self,bcd):
        high4 = (bcd &0xF0) >> 4
        low4 = bcd &0x0F
        return high4*10 +low4
        return 'hex'
    def hex2bcd(self,hex):
        high4 = hex /10
        low4 = hex %10
        result = (high4 << 4)  | low4
        return result
    def getRtcTime(self):
        buf = os.popen(self.rtc_get_time_cmd).readlines()
        # print buf
        if len(buf) >= 2:
            self.rtc_raw_time = buf[1].split(":")[1]
        # print buf
        raw_time =  self.rtc_raw_time.split()
        # print raw_time
        self.rtc_bcd_time['control1'] =  int( raw_time[self.rtc_reg_control_1] ,16)
        self.rtc_bcd_time['control2'] =  int( raw_time[self.rtc_reg_control_2] ,16)
        self.rtc_bcd_time['second'] =   int(raw_time[self.rtc_reg_second],16) &0x7F
        self.rtc_bcd_time['minute'] =   int(raw_time[self.rtc_reg_minute],16) &0x7F
        self.rtc_bcd_time['hour'] =     int(raw_time[self.rtc_reg_hour],16) &0x3F
        self.rtc_bcd_time['day'] =      int(raw_time[self.rtc_reg_day],16) &0x3F
        self.rtc_bcd_time['week'] =     int(raw_time[self.rtc_reg_week],16) &0x07
        self.rtc_bcd_time['month'] =    int(raw_time[self.rtc_reg_month],16) &0x1F
        self.rtc_bcd_time['year'] =     int(raw_time[self.rtc_reg_year],16)

        self.rtc_bin_time["control1"] = self.bcd2hex(self.rtc_bcd_time['control1'])
        self.rtc_bin_time["control2"] = self.bcd2hex(self.rtc_bcd_time['control2'])
        self.rtc_bin_time["second"] = self.bcd2hex(self.rtc_bcd_time['second'])
        self.rtc_bin_time["minute"] = self.bcd2hex(self.rtc_bcd_time['minute'])
        self.rtc_bin_time["hour"] = self.bcd2hex(self.rtc_bcd_time['hour'])
        self.rtc_bin_time["day"] = self.bcd2hex(self.rtc_bcd_time['day'])
        self.rtc_bin_time["week"] = self.bcd2hex(self.rtc_bcd_time['week'])
        self.rtc_bin_time["month"] = self.bcd2hex(self.rtc_bcd_time['month'])
        self.rtc_bin_time["year"] = self.bcd2hex(self.rtc_bcd_time['year'])




    def showTime(self):
        # date -s "2008-08-08 12:00:00"
        string_time = 'date -s "%d-%d-%d-%d-%d-%d"  '%(self.rtc_bin_time["year"],
                self.rtc_bin_time["month"],
                self.rtc_bin_time["day"],
                self.rtc_bin_time["hour"],
                self.rtc_bin_time["minute"],
                self.rtc_bin_time["second"])
        print string_time ,
        print self.rtc_bin_time['week']

    def syncToSys(self):
        string_time = 'date -s "%d-%d-%d %d:%d:%d"  '%(self.rtc_bin_time["year"],
                self.rtc_bin_time["month"],
                self.rtc_bin_time["day"],
                self.rtc_bin_time["hour"],
                self.rtc_bin_time["minute"],
                self.rtc_bin_time["second"])
        os.system(string_time)
        os.system('clock -w')
    def setRtcReg(self,reg,value):
        if reg < 0 or reg > 16 :
            raise Exception("")
        cmd = "i2cset -y -f 0 0x51 %d %d b" %(reg,value)
        os.system(cmd)

        pass
    def setSystemRtc(self,string_time):
        '''
        Args:
            string_time: "2008-08-08 12:00:00"
        Returns:
        '''
        try:
            temp = string_time.split()
            in_date = temp[0]
            in_time = temp[1]
            print in_date
            print in_time

            in_date = in_date.split('-')
            in_time =  in_time.split(":")

            self.rtc_bin_time["second"] =   int(in_time[2],10)
            self.rtc_bin_time["minute"] =   int(in_time[1],10)
            self.rtc_bin_time["hour"] =     int(in_time[0],10)


            self.rtc_bin_time["day"] =      int(in_date[2],10)
            self.rtc_bin_time["month"] =    int(in_date[1],10)
            self.rtc_bin_time["year"] =     int(in_date[0],10) %100 #just support 0~99
            self.rtc_bin_time["week"] = 0
            print self.rtc_bin_time
        except Exception as inst :
            print("input time format or data error -> %s"%inst)
            return False
        self.setSysTime(string_time)
        week = self.getLocalWeek()

            #self.rtc_bcd_time["control1"] = self.hex2bcd(self.rtc_bin_time['control1'])
            #self.rtc_bcd_time["control2"] = self.hex2bcd(self.rtc_bin_time['control2'])
        print 'year -> ' ,self.rtc_bin_time["year"]

        self.rtc_bcd_time["second"] = self.hex2bcd(self.rtc_bin_time['second'])
        self.rtc_bcd_time["minute"] = self.hex2bcd(self.rtc_bin_time['minute'])
        self.rtc_bcd_time["hour"] = self.hex2bcd(self.rtc_bin_time['hour'])
        self.rtc_bcd_time["day"] = self.hex2bcd(self.rtc_bin_time['day'])
        self.rtc_bcd_time["week"] = self.hex2bcd(self.rtc_bin_time['week'])
        self.rtc_bcd_time["month"] = self.hex2bcd(self.rtc_bin_time['month'])
        self.rtc_bcd_time["year"] = self.hex2bcd(self.rtc_bin_time['year'])

        # rtc_reg_control_1   = 0
        # rtc_reg_control_2   = 1
        # rtc_reg_second      = 2
        # rtc_reg_minute      = 3
        # rtc_reg_hour        = 4
        # rtc_reg_day         = 5
        # rtc_reg_week        = 6
        # rtc_reg_month       = 7
        # rtc_reg_year        = 8

        self.setRtcReg( self.rtc_reg_second   ,self.rtc_bcd_time[ "second" ] )
        self.setRtcReg( self.rtc_reg_minute   ,self.rtc_bcd_time[ "minute" ] )
        self.setRtcReg( self.rtc_reg_hour   ,self.rtc_bcd_time[ "hour" ] )
        self.setRtcReg( self.rtc_reg_day   ,self.rtc_bcd_time[ "day" ] )
        self.setRtcReg( self.rtc_reg_month   ,self.rtc_bcd_time[ "month" ] )
        self.setRtcReg( self.rtc_reg_year   ,self.rtc_bcd_time[ "year" ] )
        self.setRtcReg( self.rtc_reg_week   ,week )

    def setSysTime(self,string_time):
        try:
            dat = 'date -s "%s"'%(string_time)
            print dat
            os.system(dat)
        except Exception as inst :
            print ("set sys time error ->%s"%inst)
            return False
    def getLocalWeek(self):
        return time.localtime().tm_wday


    def getNetTime(self,server="www.beijing-time.org"):
        try:
             conn = httplib.HTTPConnection(server)
             conn.request("GET", "/time.asp")
             response = conn.getresponse()
             print response.status, response.reason
             if response.status == 200:
                #解析响应的消息
                result = response.read()
                # print(result)
                ts=  response.getheader('date') #获取http头date部分
                # 将GMT时间转换成北京时间
                # print ts
                ltime= time.strptime(ts[5:25], "%d %b %Y %H:%M:%S")
                # print(ltime)
                ttime=time.localtime(time.mktime(ltime)+8*60*60)
                # print(ttime)
                dat='date -s "%u-%02u-%02u %02u:%02u:%02u" '%(ttime.tm_year,ttime.tm_mon,ttime.tm_mday,ttime.tm_hour,ttime.tm_min,ttime.tm_sec)

                print dat
                #open it when in board
                os.system(dat)
                return True
             else :
                 print ("get network time error ->%s"%response.status)
                 return False
        except Exception as inst:
             print ("net time except ->%s "%inst)
             return False





if __name__  ==  "__main__" :
    parser = OptionParser()
    parser.add_option("-s", "--settime",
                    help="set time in following format : 2006-11-12 11:23:34")
    parser.add_option("-c", "--clear", action="store_true",
                    dest="clear",
                    default='n',
                    help="http request type,just support get & post")
    parser.add_option("-n", "--nettime", action="store_true",
                    help="try get time from network first")

    (options, args) = parser.parse_args()
    print options ,type(options)
    check = CheckTime()
    if options.settime  != None :
        print options.settime
        check.setSystemRtc(options.settime)
    else :
        if check.getNetTime() :
            print "check time ready "
        else :
            print "the system time is error"
    # print check.getLocalWeek()

    while True :
        time.sleep(1)
        check.getRtcTime()
        check.showTime()