#!/usr/bin/env  python
#-*- coding: utf-8 -*- 

import xml.etree.ElementTree as ET
import xml.dom.minidom as Dom
from xml.dom import minidom
import sys


node_example = '''
<root>
<testcase name="11">fuck</testcase>

</root>
'''
def get_node_from_string(node_string):
    root = ET.fromstring(node_string)
    node =  root.findall("testcase")[0]
    print node.tag
    print node.text
    print node.attrib["name"]
    node.attrib["name"] = "hello1"
    print ET.tostring(node)
    
    return ET.tostring(node)
    

def listall_testcase_node_by_minidom(file_path):
    root = minidom.parse(file_path)
    childs = root.getElementsByTagName("testcase")
    root.removeChild(childs)
    
    clone_node = dom.cloneNode(childs[0])
    
    for tmp in childs :
        
        print "node ->",
        print tmp.tagName + " :",
        print tmp.nodeName+ " :",
        print tmp.getAttribute("name")+ " :",
        print tmp.hasAttributes()
        print tmp.setAttribute("name","fuck")
#         print tmp.getAttribute["name"]
#     print dom.toxml()
    pass
    
    
def read_xml(text):  
    '''''读xml文件'''  
    # 加载XML文件（2种方法,一是加载指定字符串，二是加载指定文件）      
    # root = ElementTree.parse(r"D:/test.xml")  
    root = ElementTree.fromstring(text)  
      
    # 获取element的方法  
    # 1 通过getiterator   
    lst_node = root.getiterator("person")  
    for node in lst_node:  
        print_node(node)  
          
    # 2通过 getchildren  
    lst_node_child = lst_node[0].getchildren()[0]  
    print_node(lst_node_child)  
          
    # 3 .find方法  
    node_find = root.find('person')  
    print_node(node_find)  
      
    #4. findall方法  
    node_findall = root.findall("person/name")[1]  
    print_node(node_findall)  

help_msg = '''app read/write dom/et/sax  file
'''
if __name__ == "__main__" :
    dom1 = minidom.parse("/nfs/TestLinkVideo/GPU/template_gpu.xml")
    dom2 = minidom.parse("/nfs/TestLinkVideo/GPU/gpu_bonnie.xml")

    for i in range(1,5) :
        dom2.childNodes[0].setAttribute("name","gpu--> %s"%(i))
        x = dom1.importNode(dom2.childNodes[0], True)
        dom1.childNodes[0].appendChild(x)
    tofile = dom1.toxml("utf-8")
    fd = open("/nfs/TestLinkVideo/GPU/gpu1.xml","w")
    fd.write(tofile)
    fd.close()
    
    exit(1)
    print "xml tools"
    print sys.argv
    if len(sys.argv) < 4:
        print help_msg
        exit(0)
#     get_node_from_string(node_example)
    if(sys.argv[1] == "read" and sys.argv[2] == "dom") :
        listall_testcase_node_by_minidom(sys.argv[3])
    