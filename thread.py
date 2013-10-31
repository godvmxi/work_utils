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
    
class ThreadClass(threading.Thread):
    def run(self):
        time.sleep(2)
        now = datetime.datetime.now()
        print "%s says Hello World at time: %s" % (self.getName(), now)

#for i in range(5):
#  t = ThreadClass()
#  t.start()
lock = thread.allocate_lock()
#lock.release()
#lock.realse()
print lock.locked()
call_num = 0


            
            
    
def hello(a,b):
    global lock 
    global call_num
    call_num = call_num+1
    try :
        if lock.acquire(False) == False:
    
            print "acquire false"
            return
        else :
            print "?????"
    except :
        print "get lock exception"
        lock.release()
    print a
    print b
    print 'call num -> %d '%(call_num)
    
    print '0'
    time.sleep(2)
    print '1'
    time.sleep(2)
    print '2'
    time.sleep(2)
    print '3'
    print lock
    
    lock.release()
def hello2(a):


    print a


 
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




##while True:
#thread.start_new_thread(hello,(time.asctime(),'hello_1'))
#time.sleep(1)
#print 'wait on loop'
#thread.start_new_thread(hello,(time.asctime(),'hello_1'))
#time.sleep(1)
#print 'wait on loop'
#thread.start_new_thread(hello,(time.asctime(),'hello_1'))
#time.sleep(1)
#print 'wait on loop'
#thread.start_new_thread(hello,(time.asctime(),'hello_1'))
#time.sleep(1)
#print 'wait on loop'
#thread.start_new_thread(hello,(time.asctime(),'hello_1'))
#time.sleep(1)
#print 'wait on loop'

#func = func_thread(hello2,('hello1','hello2'))
#func.start()
#time.sleep(0.5)
#func.start()
#time.sleep(0.5)
#func.start()
#time.sleep(0.5)
#func.start()
#time.sleep(0.5)
#func.start()
#time.sleep(0.5)
#print 'exit  %d'%(call_num)
#time.sleep(100)

default_file = '/etc/sysconfig/p32p1.default'
target_file = '/etc/sysconfig/network-scripts/ifcfg-p32p1'
if os.path.exists(default_file) == False :
    shutil.copyfile(target_file,default_file)
else :
    shutil.copyfile(default_file,target_file)


    

    



