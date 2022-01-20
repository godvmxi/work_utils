import sys
import json

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart, MIMEBase
from email.mime.application import MIMEApplication
import smtplib
import time
import json
import re
from Crypto.Cipher import AES
import binascii
import random
import json


scbu_diags_email_info=""


class CryptoUtils():
    def __init__(self,key = None):
        self.origin_key = key
        self.key = self.get_encrypt_key(key).encode("utf-8")
        self.mode = AES.MODE_CBC
        #print("real key-> ", self.key)

    #加密函数，如果text不足16位就用空格补足为16位，
    #如果大于16当时不是16的倍数，那就补足为16的倍数。
    def encrypt(self,text):
        #print("encrypt text ->",len(text))
        text_array = binascii.b2a_hex(text.encode("utf-8"))
        #print("text array->",text_array)
        #print("text array size->",len(text_array))
        cryptor = AES.new(self.key,self.mode,b'0000000000000000')
        #这里密钥key 长度必须为16（AES-128）,
        #24（AES-192）,或者32 （AES-256）Bytes 长度
        #目前AES-128 足够目前使用
        length = 16
        count = len(text)
        if count < length:
            add = (length-count)
            #\0 backspace
            text = text + ('\0' * add)
        elif count > length:
            add = (length-(count % length))
            text = text + ('\0' * add)
        self.ciphertext = cryptor.encrypt(text.encode("utf-8"))
        #因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        #所以这里统一把加密后的字符串转化为16进制字符串
        hex_array = binascii.b2a_hex(self.ciphertext)
        #print("hex array-> ", hex_array)
        hex_str = hex_array.decode(encoding='utf-8')
        #print("hex str -> ", hex_str)
        return hex_str

    #解密后，去掉补足的空格用strip() 去掉
    def decrypt(self,in_text):
        cryptor = AES.new(self.key,self.mode,b'0000000000000000')
        bin_array = binascii.a2b_hex(in_text)
        #print("crypt_data ->", in_text)
        #print("crypto_text_array->", bin_array)
        plain_text  = cryptor.decrypt(bin_array).decode("utf-8")
        #print("dec_plain_text ->", plain_text)
        return plain_text.rstrip('\0')
    def decrypt_with_key(self, in_text, key):
        dec_key = self.get_encrypt_key(key)
        bin_array = binascii.a2b_hex(in_text)
        #print("dec key-> ",dec_key)
        #print("crypt_data ->", in_text)
        #print("crypto_text_array->", bin_array)
        #crypt_data = in_text.encode("utf-8")

        cryptor = AES.new(dec_key.encode("utf-8"),self.mode,b'0000000000000000')
        plain_text  = cryptor.decrypt(bin_array).decode("utf-8")
        return plain_text.rstrip('\0')
        pass
    def decrypt_string(self, in_raw_string):
        json_dat = json.loads(in_raw_string)
        #print(json_dat)
        return self.decrypt_with_key(json_dat["dat"], json_dat["key"])

        pass
    def encrypt_file(self, file):
        with open(sys.argv[2]) as fd:
            plain_text = fd.read(1024)
            #print("file content -> ", len(plain_text))
            #print("file content size ->", plain_text, "<-")
            enc_out = self.encrypt(plain_text) #加密
            #print(type(enc_out))
            #print("key：",key_str)
            #print("plain：",plain_text)
            #print("enc out：",enc_out)
            ##print(type(enc_out))
            out_data={"key": self.origin_key}
            #temp = enc_out.decode("utf-8")
            out_data["dat"] = enc_out
            ##print(out_data)
        crypt_out_text =  json.dumps(out_data)
        return crypt_out_text
    def get_encrypt_key(self, in_str):
        self.origin_plain_key =  in_str
        ##print("origin key: ->", self.origin_plain_key)
        reserver_str = self.reverse_str(self.origin_plain_key)
        ##print("reserver str-> ", reserver_str)
        out_str = ""
        for i in range(0, len(reserver_str)):
            if i % 2 == 0 :
                ###print("upper")
                out_str += reserver_str[i].upper()
            else:
                ###print("lower")
                out_str += reserver_str[i].lower()
        #print("real key-> ", out_str)
        return out_str
        pass
    def get_decrypt_key():
        pass
    def reverse_str(self,origin):
        strList = list(origin)
        strList.reverse()
        out_str =  ''.join(strList)
        return out_str
def generate_random_str(randomlength=16):
    return "keyskeyskeyskeys"
    """
    生成一个指定长度的随机字符串
    """
    random_str = ''
    base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz,.'
    length = len(base_str) - 1
    for i in range(randomlength):
        random_str += base_str[random.randint(0, length)]
    return random_str
class MailUtils():
    def __init__(self):

        crypto_inst = CryptoUtils("password")
        dec_text = crypto_inst.decrypt_string(scbu_diags_email_info)
        #print("dec_text -> ", dec_text)
        self.key_data =json.loads(dec_text)
        #print("key_data->", self.key_data)
        mail_data = self.key_data["mail"]
        self.user = mail_data["user"]
        self.passwd =  mail_data["passwd"]

    def hello(self):
        print("hello")
        pass
    def SendEmail(self, receiver_list, title, mail_body, attach_list):
        sender = self.key_data["mail"]["user"]
        sender_passwd = self.key_data["mail"]["passwd"]
        msg = MIMEMultipart()
        subject=title
        msg["From"] = sender
        msg["To"] = ",".join(receiver_list)
        msg["Subject"] = Header(subject, "utf-8").encode()

        msg.attach(MIMEText(mail_body, "html", "utf-8",))
        try:
            for file in attach_list:
                with open(file[0],"rb") as fd:
                    attach_file = MIMEApplication(fd.read())
                    attach_file.add_header('Content-Disposition','Attachment', filename=file[1])
                    msg.attach(attach_file)
        except Exception as ex:
            print("attch file fail -> %s"%ex)
            raise Exception("attch file fail -> %s"%ex)
        try:
            smtpObj = smtplib.SMTP("atlsmtp10.testtest.com", 25)
            smtpObj.set_debuglevel(0)
            smtpObj.starttls()
            smtpObj.login(sender, sender_passwd)
            smtpObj.sendmail(sender, receiver_list, msg.as_string())
            print("Mail sent out")
            smtpObj.quit()
        except smtplib.SMTPException as ex:
            print("send email fail ->",ex)
            pass

