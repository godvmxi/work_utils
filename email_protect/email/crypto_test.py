#!/usr/bin/env python3
# -*- coding:utf-8 -*-
 
from email_utils import CryptoUtils,generate_random_str


if __name__ == '__main__':

    import sys
    if len(sys.argv) != 3:
         raise ValueError("format: python encrypt.py dec/enc text")


    if sys.argv[1] == 'dec':
        key_str = generate_random_str()
        pc = CryptoUtils(key_str) #初始化密钥
        d = pc.decrypt(sys.argv[2]) #解密
        ##print("crypto ：",sys.argv[2])
        ##print("dec out：",d)

    elif sys.argv[1] == "enc":
        key_str = generate_random_str()
        pc = CryptoUtils(key_str) #初始化密钥
        e = pc.encrypt(sys.argv[2]) #加密
        #print("plain：",sys.argv[2])
        #print("enc out：",e)
    elif sys.argv[1] == "enc2":
        key_str = generate_random_str()
        pc = CryptoUtils(key_str) #初始化密钥
        with open(sys.argv[2]) as fd :
            text = fd.read(1024)
            e = pc.encrypt(text) #加密
            #print("plain：\n",text)
            #print("enc out：",e)
    elif sys.argv[1] == "enc_file":
        key_str = generate_random_str()
        pc = CryptoUtils(key_str)
        out_text = pc.encrypt_file(sys.argv[2])
        print(out_text)
        sys.exit(0)
        #print("start decode------->")
        dec_dat = pc.decrypt_string(out_text)
        #print(type(dec_dat))
        #print("dec_dat -> ", dec_dat)
        sys.exit(1)
    elif sys.argv[1] == "dec_file":
        key_str = generate_random_str()
        pc = CryptoUtils(key_str)
        with open(sys.argv[2]) as fd :
            crypto_str = fd.read(1024)
            dec_dat = pc.decrypt_string(crypto_str)
            print(dec_dat)
