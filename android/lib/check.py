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

class Check():
    def __init__(self,ip,port):
        #print 'check init'
        self.ip = ip
        self.port = port
        self.num = 0
        self.check0 = 0
        self.check1 = 0
    def set_check(self,data):
        self.num = data['num'];
        if(self.num == 0 ):
            return 0
        elif (self.num == 1):
            self.check0 = data['check0']
        else :
            self.check0 = data['check0']
            self.check1 = data['check1']
        self.app_list = []
        self.rev = ''
    def create_xml(self,method,winid,x,y,width,height):
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
    def send_msg(self,document):
        msg = document.toprettyxml(indent = "\t", newl = "\n", encoding = "utf-8")
        address = (self.ip,self.port)
        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        sock.sendto(msg,address)
        buf = sock.recv(4096)
        #print buf        
        sock.close()
        return buf
        
    def get_app_list(self):

        
        buf = self.send_msg(self.create_xml("9","2","0","0","0","0"))

        root = ElementTree.fromstring(buf)

        #print 'i am not die'
        self.state = root.find("state").text.encode('gb2312') 
         

        appNodes = root.findall('data/app')
        #print appNodes
        
        self.app_list = []
        
        for app_node in appNodes :
            app = {}
            #print app_node.find("cmd").text.encode('gb2312') 
            #app['cmd']  = app_node.find('cmd').text
            app['pid']  = int (app_node.find('pid').text.encode('gb2312') )
            #app['winid']  = int ( app_node.find('winid').text.encode('gb2312') )
            x  = int ( app_node.find('x').text.encode('gb2312') )
            y  = int ( app_node.find('y').text.encode('gb2312') )
            width  = int ( app_node.find('width').text.encode('gb2312')  )
            height  = int ( app_node.find('height').text.encode('gb2312') )
            app['rect'] = [width,height,x,y];
            horz =  app_node.find('horz').text.encode('gb2312') 
            vert =  app_node.find('vert').text.encode('gb2312') 
            if(horz == "1" and vert == "1" ):
                app['max'] = 1
            else :
                app['max'] = 0
            self.app_list.append(app) 
        return self.app_list  
        #print self.app_list
    
    def exec_check(self):
        state = False;
        self.get_app_list();
        print self.check0
        for app in self.app_list:
            print app
        return False;
            
            
       
            



    
    
   


    
    
