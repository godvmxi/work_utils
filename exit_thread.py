#!/usr/bin/env python 
import time
import os ,sys
import threading 
import shutil
try:
    import thread
except ImportError:
    import dummy_thread as thread




import datetime

import threading
import time


class MyThread(threading.Thread):
    def __init__(self, no, interval):
        threading.Thread.__init__(self)
        self.no = no
        self.interval = interval

    def run(self):
        while self.interval > 0:
            print "ThreadObject (%d) : total time(%d)\n"%(self.no, self.interval)
            time.sleep(1)
            self.interval -= 1


def test():
    thread1 = MyThread(1, 10)
    thread2 = MyThread(2, 20)
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    time.sleep(2)
    


    
import subprocess

    

class ThreadClass(threading.Thread):
    def run(self):
        time.sleep(2)
        now = datetime.datetime.now()
        print "%s says Hello World at time: %s" % (self.getName(), now)


            
            
    
def hello(a,b):
    global lock 
    global call_num
    print "hello1"
    
    print '0'
    time.sleep(2)
    print '1'
    time.sleep(2)
    print '2'
    time.sleep(2)
    print '3'
    print lock

def hello2(a):
 
    print '0'
    time.sleep(2)
    print '1'
    time.sleep(2)
    print '2'
    time.sleep(2)
    print '3'
    
class func_thread():
    call_num = 0
    def __init__(self,function,argv):
        pass
        self.lock =  thread.allocate_lock()
        self.func = function
        self.argv = argv
        self.call_num = 0
        
    def start(self):
        self.call_num+=1
        print self.argv
        thread.start_new_thread(self.thread_function, self.argv)

    def thread_function(self,arg0,arg1):
        try :
            if self.lock.acquire(False) == False:
                print "acquire lock false"
                return
        except :
            print "get lock exception"
            self.lock.release()
        print "get lock and run"
        self.func(self.argv)
        self.lock.release()
        print 'call num -> %d' %(self.call_num)



import threading
import ctypes


def _async_raise(tid, exctype):
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("nonexistent thread id")
    elif res > 1:
        # if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect
        ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), 0)
        raise SystemError("PyThreadState_SetAsyncExc failed")

    
class Thread(threading.Thread):
    def set(self,func):
        self.thread_func = func
    def raise_exc(self, excobj):
        assert self.isAlive(), "thread must be started"
        for tid, tobj in threading._active.items():
            if tobj is self:
                _async_raise(tid, excobj)
                return
        # the thread was alive when we entered the loop, but was not found 
        # in the dict, hence it must have been already terminated. should we raise
        # an exception here? silently ignore?
        
    def terminate(self):
        # must raise the SystemExit type, instead of a SystemExit() instance
        # due to a bug in PyThreadState_SetAsyncExc
        self.raise_exc(SystemExit)
    def run(self):
        self.index = 0
        self.thread_func()
            
counter = 0
mode = 'ap'
def __clear_dns():
    fd = open("/etc/resolv.conf","w")
    fd.close()
    print "old dns -> ",
    print os.popen('''  cat /etc/resolv.conf |grep -v "nerated" |grep -v "NOTE" |grep -v "recognized" ''').readlines()
def __clear_interface_br0():
    '''
    clear the br0 ip setting 
    '''
    os.system("killall -9 dhclient")
    time.sleep(1)
    os.system("killall -9 dhclient")
    os.system("ps aux |grep dhclient")
    os.system('ip addr flush dev br0 ')
    os.system('ip addr flush dev p32p1 ')
    
    pass    
def __add_dhclient_conf():
    '''
    add config file for dhclient 
    '''
    mac = os.popen(''' ip addr show dev p8p1 |grep link |awk '{print $2}' ''' ).read()
    if len( mac ) > 0:
        print "add "
        dat = 'send dhcp-client-identifier %s ;  ' %(mac)
        fd  = open(''' /etc/dhcp/dhclient.conf ''',"w")
        fd.write(dat)
        fd.close()
        return 
    pass
def __run_br0_auto_mode():
    print "hello"
    __clear_dns()
    __clear_interface_br0()    
    
    os.system(" /sbin/dhclient -4 br0")
    ipv4 = os.popen('''  cat /etc/resolv.conf |grep -v "nerated" |grep -v "NOTE" |grep -v "recognized" ''').readlines()
    
    os.system(" /sbin/dhclient -6 br0")
    ipv6 = os.popen('''  cat /etc/resolv.conf |grep -v "nerated" |grep -v "NOTE" |grep -v "recognized" ''').readlines()
    dns = []        
    dns = ipv4 +ipv6

    dns = list( set(dns) )
    dns = [";  Generate by Network Framework Api\n"] + dns
    os.system("killall -9 dhclient")
    time.sleep(1)
    os.system("killall -9 dhclient")
    fd = open("/etc/resolv.conf","w")
    fd.writelines(dns)
    fd.close()
    
def __run_eth0_mode():
    pass

def apply__setting():
    global mode
    os.system("killall -9 dhclient")
    time.sleep(0.5)
    os.system("killall -9 dhclient")
    if mode == "ap":        
        __run_br0_auto_mode()
        
        
        pass
    elif mode == "client" or mode == "off" :
        #just restart interface
        pass
    elif mode == "invalid":
        pass
    else :
        pass
        
    
        
def fuck2():
    index = 1
    while True:
        print "fuck2 --> %d    "%(index)
        index += 1
        time.sleep(1)
def timer_second():
    global counter 
    counter += 1
    threading.Timer(1, timer_second).start()
               
if __name__ == '__main__':
    
    __run_br0_auto_mode()
    
    exit()
    
    threading.Timer(1, timer_second).start()

    test1 = Thread()
    test1.set(apply__setting)
    test1.start()
    test2 = Thread()
    test2.set(fuck2)
    test2.start()
    print "sleep 2"
    time.sleep(6)
    print "try to kill test1"
    test1.terminate()
    while True :
        time.sleep(1)
        if test1.isAlive():
            print "still alive"
        else :
            print "exit"
            exit(1)
        

    

    



