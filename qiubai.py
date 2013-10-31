#!/usr/bin/env python
#coding:utf-8
import urllib2
import re
class qiubai:
    def __init__(self,page=1):
        self.page=page
    def search(self,page):
        url = "http://www.qiushibaike.com/week/page/%s" % page
        re_qb = re.compile(r'detail.*?<a.*?>(.*?)<.*?title="(.*?)">\s*(.*?)\s*?<',re.DOTALL)
        html = urllib2.urlopen(url).read()
        my_qiubai = re_qb.findall(html)
        for i in range(0,19):
           for k in range(3):
                print my_qiubai[i][k]
        s = raw_input("回车继续")
        if s == "q":
            exit()
        else:
            page=int(page)+1
            print "-"*18 + "第" + str(page) + "页" + "-"*18
            self.search(page)
        print "-"*40
    def query(self):
        global p
        p = raw_input("输入要看的页数:")
        if p == "q":
            exit()
        elif not p.isdigit() or p =="0":
            self.query()
        else:
            print "-"*18 + "第" + p + "页" + "-"*18
            self.search(p)
if __name__ == "__main__":
    print "-"*40
    print "糗百命令行版"
    print '输入"q"退出程序'
    print "-"*40
    qb=qiubai()
    qb.query()