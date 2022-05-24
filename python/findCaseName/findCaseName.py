#!/usr/bin/env python
import os

from xml.etree import ElementTree

import sys

def get_all_result_files(case_dir):
    cmd = "find " + case_dir + ' -name "VisionResults.xml"'
    buf = os.popen(cmd)
    file_list = buf.readlines()
    return file_list
def read_file_content(fpath):
    fd = open(fpath)

    #print fd.readlines()
    return fd.read()
def parse_xml_result_by_et(xml_text):
    et_root = ElementTree.fromstring(xml_text)
    names=   et_root.findall("Name")  
    for name in names :
        print "case name --> ",
        print name.text,
    names=   et_root.findall("Variant/Result")  
    for name in names :
        print "\t\tresult --> ",
        print name.text,
        
    names=   et_root.findall("Variant/Name")  
    for name in names :
        print "\t\tVariant name --> ",
        print name.text
        
#     names=   et_root.findall("Variant/File/Name")  
#     for name in names :
#         print "\t\tOutput name --> ",
#         print name.text

    

if __name__ == "__main__" :
    if len( sys.argv) < 2:
        print "input case dir"
        exit(1)
    if os.path.isdir(sys.argv[1]) == False :
        print "input dir not exist"
        exit(1)
    filelist = get_all_result_files(sys.argv[1])
    for file in filelist :
        file = file.replace("\n","")
        content = read_file_content(file)
        parse_xml_result_by_et(content)
