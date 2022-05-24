#!/bin/env python

try :
    assert 1==1 ,"excetion occur"
    print "no exception"
except AssertionError as inst:
    print inst
    
bssidNum = 4    
for index in [2,3,4] :
#    print "current index -> %s" %(index)
    for bssidNum in [2,3,4] :
#        print " %s -- %s " %(index,bssidNum)  
        if index == bssidNum :
            print "delete   %s -> %s " %(index,bssidNum)
            pass
        elif index > bssidNum :
#            print "error index "
            pass
        else :   
            print "deal  %s --> %s " %(index,bssidNum)     
            for old in range(index,bssidNum+1) :
                print "       replace %s -- %s " %(index,old)
                if old == index :
                    print "            delete "