#!/bin/env python3
import sys
import locale
import requests
from lxml import etree
import pprint
import os
import time
import shutil
def handle_image_line(line, img_dir, index):
    line = line.replace("\n", "").replace("![](","").replace(")","").replace(" ", "")
    print("will handle line -> " + line)
    link_name = line
    file_name = line.split("/")[-1]
    
    post_fix = file_name.split(".")[-1]
    if len(post_fix) > 0:
        post_fix = post_fix.lower()
    final_file_name = None

    print("link file_name -> " + file_name + "  post->" + post_fix + "<-")
    cmd = None
    if line.find("img-blog") > 0:
        link_name = link_name.split("?")[0]
        file_name = link_name.split("/")[-1]
        
        target_file_name = img_dir + "/" + file_name
        print("csdn img link name:" + link_name)
        print("csdn file name : " + file_name)
        print("target_file_name: " + target_file_name)
        cmd="wget %s -O %s"%(link_name, target_file_name)
    elif post_fix in ["png", 'jpg', 'jpeg', "gif"]:
        target_file_name = img_dir + "/" + file_name
        print("##normal target file : "+ target_file_name)
        cmd =  "wget %s -O %s"%(link_name, target_file_name)
    else:
        print("downlink is not support")
        sys.exit(0)
    print("will run cmd: " + cmd)
    os.system(cmd)
    line = "![](%s)\n"%file_name
    time.sleep(2)
    return line
    pass
def process_origin_markdown(source_dir, file_name, target_dir, index):
    #img_dir = target_dir  + "/csdn_" + file_name.replace(".md", "")
    #target_file = target_dir + "/csdn_" + file_name
    img_dir = "%s/z_csdn_%03d_%s"%(target_dir, index, file_name.replace(".md", ""))
    target_file = "%s/z_csdn_%03d_%s"%(target_dir, index, file_name)
    print("target file   -> " + target_file)
    print("target img dir-> " + img_dir)
    #os.remove(target_file)
    shutil.rmtree(path = img_dir,ignore_errors=True)
    os.mkdir(img_dir)
    out_lines = []
    with open(source_dir + "/" +file_name, "r")  as fd:
        lines = fd.readlines()
        for line in lines:
            if line.startswith("link"):
                continue
            if line.startswith("keywords:"):
                line = "keywords: CSDN\n"
            if line.startswith("![]") : 
                line = handle_image_line(line, img_dir, index) + "\n"
                print("img line : " + line)
            out_lines.append(line)
    if len(out_lines) > 0 :
        with open(target_file, "w+")  as fd:
            fd.writelines(out_lines)
        

if __name__ == "__main__":
    source_dir = sys.argv[1]
    target_dir = sys.argv[2]
    start_files = int(sys.argv[3])
    end_files = int(sys.argv[4])
    source_file_list = os.listdir(source_dir)
    #pprint.pprint(source_file_list)
    index = 1
    for file in source_file_list :
        if index > end_files:
            break
        print("########################## handle file -> start: %3d end:%3d index:%3d file: %s"%(start_files,end_files, index, file))
        if index >= start_files:
            process_origin_markdown(source_dir,  file, target_dir,index)
        index  = index + 1

