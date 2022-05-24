import dbus 
import os
import time
from IPy import IP

 
eth0 = 'p32p1'

class CPGMgt_Service_NetworkSettingObject():
    test = 1    
    def __init__(self):
        CPGMgt_Service_NetworkSettingObject.test = CPGMgt_Service_NetworkSettingObject.test +1 
        pass
    def get(self):
        print CPGMgt_Service_NetworkSettingObject.test;
        pass
    def set(self):
        pass
    

INIT_CONFIG_VALUE = dbus.Array( [                                
                          
                                    ['wirelessIPv4','auto'],
                                    ['wirelessIPv6','disable'],
                                    
                                    ['wirelessAddress4',''],
                                    ['wirelessAddress6',''],
                                    ['wirelessGateway4',''],
                                    ['wirelessGateway6',''],
                                    
                                    
                                    ['wiredIPv4','auto'],
                                    ['wiredIPv6','disable'],
                                    
                                    ['wiredAddress4',''],
                                    ['wiredAddress6',''],
                                    ['wiredGateway4',''],
                                    ['wiredGateway6',''],
                                    
                                              
                                    ['dns4',''],
                                    ['dns6','']])


class UpdateFile():
    def __init__(self,name):
        self.buf = []
        self.split = '='
        self.name = name
        pass
    def update_line(self,key,value):
        tmp = []
        state = False
        for line in self.buf :
            dat = line.split(self.split)
            if dat[0] == key :
                line = '%s=\"%s\"\n'%(key,value) 
                state = True #find key and just update line
            tmp.append(line)
        if  state == False: #insert line
            line = '%s=\"%s\"\n'%(key,value) 
            tmp.append(line)
            
        self.buf = tmp
        return state
    def remove_line(self,key):
        tmp = []
        state = False
        for line in self.buf :
            dat = line.split(self.split)
            if dat[0] == key :
                #line = '%s=%s\n'%(value[0],value[1]) 
                state = True #find key and just update line
            else :
                tmp.append(line)
        self.buf = tmp
        return state
    def read_file(self):
        fd = open(self.name)
        self.buf = fd.readlines()
        fd.close()
 
    def save_file(self):
        fd = open(self.name,'w')
        fd.writelines(self.buf)
        fd.close()

    def update_lines(self,lines):
        self.read_file()
        for line in lines :
            if line[1] == '':
                self.remove_line(line[0])
            else :
                self.update_line(line[0], line[1])
        self.save_file()
    def show_file(self):
        for line in self.buf :
            print line
        
        
        
        pass
    

 
if __name__ == '__main__' :   
#    test = UpdateFile('/home/bluebird/test')
#    dat = [['ADDRESS','192.168.0.2'],['IPV4','MANUAL'],['inset','']]
#    test.update_lines(dat)
#    test.read_file()
#    print '\n\nnew----->\n'
#    test.show_file()

    ip = '10.140.28.32'
    mask = '255.255.255.0'
    print IP(ip).make_net(mask)



