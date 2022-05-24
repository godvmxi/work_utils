#!/bin/env python3
import sys
import locale
import requests
from lxml import etree
import pprint
import os
import time

print(sys.getfilesystemencoding())
print(locale.getpreferredencoding())

def get_acticle_list(user, page_start, page_end):
    
    #paras["page": "1"]
    #headers = {}
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36"
}

    #headers["user-ganet"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
    #headers["accept"] = """application/json, text/plain, */*"""
    #headers["origin"] = "https://mp.csdn.net"
    #headers["accept-language"] = "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    #headers["Content-Type"] = "text/text; charset=utf-8"
    link_list = []
    for index in range(int(page_start), int(page_end)+1 ):
        print(index)
        base_url= "https://blog.csdn.net/godvmxi/article/list/%s"%index


        res = requests.get(url = base_url,headers=headers)
        print(res.url)
        print(res.status_code)

    #print(res.content)
    #print(res.content)
        page_html = etree.HTML(res.content)
        article_list = page_html.xpath('//*[@id="articleMeList-blog"]/div[2]')[0]
        print(len(article_list))
        for obj in article_list:
            id =  obj.attrib["data-articleid"]
            link = "https://blog.csdn.net/godvmxi/article/details/%s\n"%id
            link_list.append(link)
    pprint.pprint(link_list)
    with open("link.txt","w")  as fd:
        fd.writelines(link_list)
    #print(len(link_list))
    return link_list
def down_load_articals(link_list):
    for link in link_list:
        link = link.replace("\n", "")
        print("Download : %s"%link)
        file_name = link.split("/")[-1]
        print("target file name->%s"%file_name)
        cmd = "clean-mark %s -o download/%s"%(link,file_name)
        print("cmd->   %s"%cmd)
        os.system(cmd)
        time.sleep(5)
        #break

if __name__ == "__main__" :
    user= sys.argv[1]
    page_start = sys.argv[2]
    page_end  = sys.argv[3]
    link_list  = get_acticle_list(user, page_start, page_end)
    down_load_articals(link_list)
    pass