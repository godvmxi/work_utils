__author__ = 'dandan'
import threading
import time




def thread_1():
    while True :
        print "thread 1"
        time.sleep(1)
def thread_2():
    while True :

        time.sleep(0.6)
        print "thread 2"


t1 = threading.Thread(target=thread_1)
t2 =  threading.Thread(target=thread_2)
print "ok"
t1.start()
t2.start()

print "???"