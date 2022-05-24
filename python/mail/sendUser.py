#!/usr/bin/env python
# -*- coding: utf-8 -*-
#导入smtplib和MIMEText
import smtplib
from email.mime.text import MIMEText
import  base64
import sys
from optparse import OptionParser
import codecs
import time

mailto_list=["bright.jiang@infotm.com","sam.zhou@infotm.com"]

########smtp setting#############
mail_host="smtp.exmail.qq.com"
mail_user="xxx@xxx.com"
mail_pass="xxx"
mail_postfix="xxx.com"
######################
def send_mail(to_list,sub,content,type='html'):
    '''
    to_list:发给谁
    sub:主题
    content:内容
    send_mail("aaa@126.com","sub","content")
    '''
    me=mail_user+"<"+mail_user+">"
    msg = MIMEText(content,_subtype=type,_charset='UTF-8')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        s = smtplib.SMTP()
        print("@@!@@")
        print s.connect(mail_host)
        print("@@!@@")
        print s.login(mail_user,mail_pass)
        print("@@!@@")
        s.sendmail(me, to_list, msg.as_string())

        s.close()
        return True
    except Exception, e:
        print("@@!@@")
        print str(e)
        return False
def get_email_title(file) :
    try :
        fd = codecs.open(file,'r','UTF-8')
        data =  fd.read()
        fd.close()
    except :
        print("read mail title error")
        sys.exit(0)
    return data
def get_email_content_template(file) :
    try :
        fd = open(file,'r')
        data =  fd.read()
        fd.close()
    except :
        print("read mail content error")
        sys.exit(0)
    return data
def get_user_list(file):
    try :
        fd = open(file,'r')
        data =  fd.readlines()
        fd.close()
        print(type(data) )
    except :
        print("read user list error")
        sys.exit(0)
    userPass = []
    for line in data :  
        if len(line) == 0 :
            break
        if line[0] in ['#',' ','\n'] :
            continue
        userPass.append(line.split() )
    return userPass
def update_email_from_template(template,userPass):
    print(type(userPass[0]))
    temp= userPass[0].split(".")
    big_name = "".join([temp[0][0:1].upper(),temp[0][1:]," ",temp[1][0:1].upper(),temp[1][1:] ] )
    print(big_name)
    template = template.replace("##USER_NAME",userPass[0]).replace("##USER_PASS",userPass[1]).replace("##USER_FULL",big_name)
    return template
if __name__ == '__main__':
    parser = OptionParser(usage="usage:%prog [optinos] filepath")
    parser.add_option("-u", "--userfile",
                    action = "store",
                    type = 'str',
                    dest = "userFile",
                    default = "user.lst",
                    help="user list file ,will delete all users not include in the file and update the password in the file"
                    )

    parser.add_option("-t", "--title",
                    action = "store",
                    type = 'str',
                    dest = "title",
                    default = "title.t",
                    help = "email tile template"
                    )
    parser.add_option("-c", "--content",
                    action = "store",
                    type = 'str',
                    dest = "content",
                    default = "mail.t",
                    help = "mail content template"
                    )
    (options, args) = parser.parse_args()
    userList = get_user_list(options.userFile)
    print (userList)

    mail_title =  get_email_title(options.title)
    mail_content = get_email_content_template(options.content)
    for user in userList :
        print user
        send_user =  "%s@infotm.com"%(user[0])
        content = update_email_from_template(mail_content,user)
##        break
        print('begin send')
        if send_mail([send_user ],mail_title,content):
            print "send to %s  ok" %(user[0])
        else:
            print "send to %s  fail" %(user[0])
