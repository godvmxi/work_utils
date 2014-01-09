import sys,time
import sys
print 
for i in range(3):
    sys.stdout.write("\r")
    sys.stdout.write("\b"*(i-1))
    print '\b'*(i-1),
    print '*'*i
#    print '\r'    

    time.sleep(1)
print 

        
