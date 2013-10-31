#-*- coding: utf-8 -*-  
#!/usr/bin/python   
import paramiko  
import threading  
import os
import time
def ssh2(ip,username,passwd,cmd):  
    try:  
        ssh = paramiko.SSHClient()  
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  
        ssh.connect( ip,22,username,passwd,timeout=5)  
        for m in cmd:  
            stdin, stdout, stderr = ssh.exec_command(m)  
#           stdin.write("Y")   #简单交互，输入 ‘Y’   
            out = stdout.readlines()  
            #屏幕输出  
            for o in out:  
                print o,  
        print '%s\tOK\n'%(ip)  
        ssh.close()  
    except :  
        print '%s\tError\n'%(ip) 

def check_host(host):
    ping =  os.popen("ping %s -c 1" %(host)).read()
    if ping.find('icmp_req') > 0:
        return True
    else :
        return False
def exec_host_cmd(host,user,passwd,cmd):

    ssh = paramiko.SSHClient()  
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  
    ssh.connect(hostname = host,username = user,password =passwd,timeout=10) 

    stdin,stdout,stderr=ssh.exec_command(cmd)
    out = stdout.readlines()
    ssh.close()
    
    
def check_and_reboot():
    live = True
    times = 0
    reboot = '/usr/bin/reboot'
    while True :
        state = check_host(host[0])
        if state != live :
            live = state
            if  state == True:
                times = times +1            
                print 'host %s -> %s ' %(host[3],times)
        if  state == True:
            exec_host_cmd(host[0],host[1],host[2],reboot)
        
        time.sleep(3)
    
            
if __name__=='__main__':  
    hosts = [['10.140.28.35','root','aDMIN123#','haiming'],
             ['10.140.28.35','root','admin123','chaguan'],
             ['10.140.28.35','root','aDMIN123#','zhiliang'],
             ['10.140.28.35','root','dan','jingliang']
             ]
    reboot = '/usr/bin/reboot'
    cmd = 'echo hello!'#你要执行的命令列表  
    username = ""  #用户名  
    passwd = ""    #密码  
    threads = []   #多线程  
    print "Begin......" 
    
    host = ['10.140.28.46','root','admin123','Guanchao']
#    ssh = paramiko.SSHClient()  
#    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  
#    ssh.connect(host[0],22,host[1],host[2],timeout=5)  

    check_and_reboot()

    while True:
        if check_host(host[0]) :
            print 'find alive,kill -> %s' %(host[3])
            exec_host_cmd(host[0],host[1],host[2],reboot)
        else :
            print 'system down'
        time.sleep(5)

        

      
    
    
    exit()
        
    for i in range(1,254):  
        ip = '192.168.1.'+str(i)  
        a=threading.Thread(target=ssh2,args=(ip,username,passwd,cmd))   
        a.start() 