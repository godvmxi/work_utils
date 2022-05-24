'''
Created on 2013-3-26  
   
@author:  dandan && chaguan
@module: domxml.genXML  
@description: 
'''    
import xml.dom.minidom as Dom
import socket
from xml.etree import ElementTree
import random
import time
import string


def create_xml(method,winid,x,y,width,height):
    doc = Dom.Document()  
    root_node = doc.createElement("root")  
    doc.appendChild(root_node)  
    
    method_node = doc.createElement("method")
    method_value = doc.createTextNode(method)
    method_node.appendChild(method_value)
    root_node.appendChild(method_node) 
    
    id_node = doc.createElement("id")
    id_value = doc.createTextNode("2")
    id_node.appendChild(id_value)
    root_node.appendChild(id_node) 
     
    src_node = doc.createElement("src")
    src_value = doc.createTextNode("source")
    src_node.appendChild(src_value)
    root_node.appendChild(src_node)  
            
    app_node = doc.createElement("app")       
    app_winid_node = doc.createElement("winid")  
    app_winid_value = doc.createTextNode(winid)  
    app_winid_node.appendChild(app_winid_value)  
    app_node.appendChild(app_winid_node)     
    app_pid_node = doc.createElement("pid")  
    app_pid_value = doc.createTextNode("22222")  
    app_pid_node.appendChild(app_pid_value)  
    app_node.appendChild(app_pid_node)       
    app_title_node = doc.createElement("title")  
    app_author_value = doc.createTextNode("33333")  
    app_title_node.appendChild(app_author_value)  
    app_node.appendChild(app_title_node)  
    root_node.appendChild(app_node) 
    
    data_node = doc.createElement("data")     
    data_x_node = doc.createElement("x")  
    data_x_value = doc.createTextNode(x)  
    data_x_node.appendChild(data_x_value)  
    data_node.appendChild(data_x_node)     
    data_y_node = doc.createElement("y")  
    data_y_value = doc.createTextNode(y)  
    data_y_node.appendChild(data_y_value)  
    data_node.appendChild(data_y_node)    
    data_width_node = doc.createElement("width")  
    data_width_value = doc.createTextNode(width)  
    data_width_node.appendChild(data_width_value)  
    data_node.appendChild(data_width_node)        
    data_height_node = doc.createElement("height")  
    data_height_value = doc.createTextNode(height)  
    data_height_node.appendChild(data_height_value)  
    data_node.appendChild(data_height_node) 
  
    root_node.appendChild(data_node)
    return doc

#create udp connection and send xml to server(openbox)
def send_msg(document):
    msg = document.toprettyxml(indent = "\t", newl = "\n", encoding = "utf-8")
    address = ('10.140.28.57',3333)
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.sendto(msg,address)
    buf = sock.recv(4096)
    #print buf
    
    sock.close()
    return buf
    
def get_winIds():
    
    buf = send_msg(create_xml("9","2","300","40","50","60"))
    root = ElementTree.fromstring(buf)
    winIds = root.findall("data/app/winid")
    #print winIds
    winids = []
    root_node = Dom.parseString(buf,None)
    data_node = root_node.getElementsByTagName("data")[0]
    app_nodes = data_node.getElementsByTagName("app")
    for app_node in app_nodes :
        winid_node = app_node.getElementsByTagName("winid")[0]
        winids.append(winid_node.childNodes[0].data) 
    #print winids
    return winids
def get_rand(min,max):
    return '%d' %(random.randint(min,max))
    
def exec_method():
    method_list = ["9","3","4","6","7","8","14","15","16"]
    apps = get_winIds();
    while 1 :
        method =  random.choice(method_list)
        app = random.choice(apps)
        #app = apps[0]
        for i in range(1,4):
            msg = create_xml(method,app,get_rand(10,1000),get_rand(10,800),get_rand(100,500),get_rand(100,500))
            send_msg(msg);
            time.sleep(0.5)
            if method == "3" :
                print("full screen "+ app)
                send_msg(msg);
                print("full screen " + app)
                time.sleep(0.5)
                #send_msg(msg);
                print("full screen "+ app)
            if method == "4":
                print("max screen "+ app)
                send_msg(msg);
                print("max screen "+ app)
                time.sleep(0.5)
                #send_msg(msg);
            if method == "6" :
                print("bottom screen "+ app)
                msg = create_xml("8",app,get_rand(10,1000),get_rand(10,800),get_rand(100,500),get_rand(100,500))
                print("normal screen "+ app)
                send_msg(msg);
            if method == "7" :
                print("bottom screen "+ app)
                msg = create_xml("8",app,get_rand(10,1000),get_rand(10,800),get_rand(100,500),get_rand(100,500))
                print("normal screen "+ app)
                send_msg(msg);
            if method == "14" :
                print("resize app "+ app)
            if method == "15" :
                print("move app "+ app)
            if method == "16" :
                print("resize & move app "+ app)
            time.sleep(1)
        


  
if __name__ == "__test__":  

    
    #send_msg(create_xml("16","2","300","40","50","60"))
    #get_winIds();
    exec_method();

    
    
   


    
    
