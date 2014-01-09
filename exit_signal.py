#!/bin/env python
import signal
import sys
import time
def term(sigNum,frame):
    print '%s--> %s-->%s '%(sys._getframe().f_code.co_name,sigNum,frame)
def exit(sigNum,frame):
    print '%s--> %s-->%s '%(sys._getframe().f_code.co_name,sigNum,frame)
def INT(sigNum,frame):
    print '%s--> %s-->%s '%(sys._getframe().f_code.co_name,sigNum,frame)
if __name__ == "__main__":
    signal.signal(signal.SIGINT,INT)
    signal.signal(signal.SIGTERM,term)
    
    while True:
        time.sleep(1)
        print "working-> %s"%time.asctime()
    