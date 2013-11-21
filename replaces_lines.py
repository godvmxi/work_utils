import os
import re
import tempfile
import shutil
import uuid

def update_lines(file_path,replace_lines):
    '''
        insert ,update ,remove lines according the Regular Expressions 
        
        Args:
            file_path
            replace_reg :list of [  Regular Expressions , new line]
                        for example :
                        [
                            ['oldline1','newline'],
                            ['oldline2','newline'],
                                ... ...
                            ['oldlinen','newline']                        
                        ]
                    oldline* should be Regular Expressions
        Returns:        
            state: 'affect lines and state'
                        state list -> []
                    state : enum string: insert/update/delete
         
        Raises:
            Exception: "file read fail"
            Exception: "file write fail"   
            Exception: "replace_lines format error"      
        '''
    if type(replace_lines) != type( [] ):
        raise Exception('replace_lines format error')
    try :
        f = open(file_path,'r')         
        file_lines = f.readlines() 
    except IOError :
        raise "file read fail" 
    f.close()
    affect_lines = 0
    for reg in replace_lines :
        if type(reg) != type([])  and len(reg) != 2:
            raise Exception('replace_lines format error')
        
        old_line = reg[0]   
        new_line = reg[1]    
        if old_line == None:
            if new_line == None :
                continue
            file_lines.append(new_line+'\n')
            print "insert new line directly"
            affect_lines += 1
            continue
        
        found_flag = False
        re_line = re.compile(r''+old_line)  
        tmp_lines = []
        for line in file_lines:
            str_line = line.strip('\n')
            if re_line.match(str_line) :
                found_flag = True
                if new_line == None :
                    print "find lines and delete"
                    affect_lines += 1
                    
                else :
                    print "find lines and replace"
                    tmp_lines.append(new_line+'\n')
                    affect_lines += 1
            else :
                print "not match line and copy old line"
                tmp_lines.append(line)
        if found_flag == False and new_line != None:
            print "insert new line for not find"
            tmp_lines.append(new_line+'\n')
            affect_lines += 1


        file_lines = tmp_lines   
    print "replace result --> "
    print file_lines     
    try :
        fd,tmpf = tempfile.mkstemp()
        print "des   --> " + tmpf
        f = open(tmpf,"w")
        f.writelines(file_lines)
        f.close()
        shutil.copy(tmpf, file_path)
        os.close(fd)       
        print 'debug start -->'
        os.system('cat %s' %(tmpf))     
        os.unlink(tmpf)        
        print 'check delete  -->'
        os.system('cat %s' %(tmpf))        
        print 'debug over  -->'
    except IOError :
        raise "file read fail" 
    
def __generate_config_file(lines):
    replace_reg = []
    for line in lines:
        if line[1] == None :
            tmp = [line[0],None]
            replace_reg.append(tmp)
        else :
            new_line = '%s=%s'%(line[0],line[1]) 
            tmp=[line[0],new_line]
            replace_reg.append(tmp)
    update_lines('/tmp/test',replace_reg)
    
    
def __get_interface_dns(iface):
    lines = os.popen('nm-tool ').readlines()
    result = []
    tmp = {}
    DNS = []    
    for line in lines :
        if line.find("Device:") > 0:
            if len(tmp) != 0:
                tmp['dns'] = DNS
                result.append(tmp)
                tmp = {}
                DNS = []
            
            line= line.split()
            tmp['dev'] = line[2]
        else :
            if line.find('DNS') > 0:
    
                line = line.split()
                DNS.append(line[1])   
                
    tmp['dns']= DNS            
    result.append(tmp)
#    pprint.pprint(result)
    for tmp in result :
        if tmp['dev'] == iface:
            return tmp['dns']
    return []
    
        
if __name__ == '__main__' :
    print __get_interface_dns('p2p1')
    
    
    
    
    
    
    
    
    exit()

    
    
    filepath = '/tmp/test' 
    open(filepath,'w').close() 


    default = '''TYPE=Ethernet
BOOTPROTO=dhcp
DEFROUTE=yes
IPV4_FAILURE_FATAL=no
IPV6INIT=yes
IPV6_AUTOCONF=yes
IPV6_DEFROUTE=yes
IPV6_FAILURE_FATAL=no
ONBOOT=yes
PEERDNS=yes
PEERROUTES=yes
IPV6_PEERDNS=yes
IPV6_PEERROUTES=yes
'''
    mac = "00:11:22:33:44:55"
    iface = 'eth0'
    uid = uuid.uuid1()
    mac_string = 'HWADDR=%s\n'%(mac)
    iface_string = 'NAME=%s\n'%(iface)
    uuid_string = 'UUID=%s\n'%(uid)
    result =  default+mac_string+iface_string+uuid_string

    f = open(filepath,"w")
    f.write(result)
    f.close()
    os.system('cat %s'%filepath)
    
    
        
    
    lines = [ 
                     ['ONBOOT','yes'],
                     ['DEFROUTE','yes'],
                     ['BOOTPROTO','dhcp'],
                     
                     ['PEERDNS','yes'],
                     ['PEERROUTES','yes'],
                     
                     ['IPADDR0',None],
                     ['PREFIX0',None],
                     ['GATEWAY0',None]
                     
                     ]
    __generate_config_file(lines)
    
#    lines = [ 
#                        ['IPV6INIT','yes'],
#                        ['IPV6_FAILURE_FATAL','no'],
#                        ['ONBOOT','yes']  ,
#                        ['IPV6_DEFROUTE','yes'],
#                        
#                        ['IPV6_AUTOCONF','yes'],
#                        ['IPV6_PEERDNS','yes'],
#                        ['IPV6_PEERROUTES','yes'],
#                        
#                        ['IPV6_DEFAULTGW',None],
#                        ['IPV6ADDR',None]
#                        ]
#    __generate_config_file(lines)
#    update_lines(filepath,lines)
    os.system('cat /tmp/test')

        

    
    
#    lines = ['helo\n','maybe\n']
#    fd,tempfile = tempfile.mkstemp()
#    print fd
#    print tempfile
#    os.close(fd)
#    f = open(tempfile,"w")
#    f.writelines(lines)
#    f.close()
#    os.system('cat %s' %(tempfile))
#    shutil.copy(tempfile, '/tmp/new')
#    os.unlink(tempfile)
#    print "delete and read"
#    os.system('cat %s' %(tempfile))
#    print "read dst"
#    os.system('cat /tmp/new ')
#    

    
    
    

        
        
            
                
                
                
    