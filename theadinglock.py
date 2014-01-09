#!/bin/env python

import threading
try:
    import thread
except ImportError:
    import dummy_thread as thread
import multiprocessing
    
lock = threading.RLock()
sem = threading.Semaphore()
mlock = multiprocessing.Lock()

mrlock = multiprocessing.RLock()



import time
    
def hello():
    print "try in"
    if  mlock.acquire(block=True,timeout=3) == False :
        print "exit"
        return 
    print "in"
    time.sleep(4)
    print 'out'
    mlock.release()
a=()
while True :
    thread.start_new_thread(hello,a)
    thread.start_new_thread(hello,a)
    thread.start_new_thread(hello,a)
    time.sleep(2)