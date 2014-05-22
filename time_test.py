import time

t =  time.time()

t1 = (2013,2,9,22,30,15,  0,365,0)
t2 = (2013,4,9,18,35,35,  0,365,0)
t3 = (2014,1,30,21,30,27,  0,365,0)
t4 = (2014,2,2,20,15,37,  0,365,0)
t5 = (2014,2,5,13,20,45,  0,365,0)



t6 = (2014,4,24,10,01,44,  0,365,0)

td1 = time.mktime(t1)
td2 =  time.mktime(t2)

td3 =  time.mktime(t3)
td4 =  time.mktime(t4)
td5 =  time.mktime(t5)
td6 =  time.mktime(t6)

print time.ctime(td1)   
print td1

print time.ctime(td2)   
print td2
print time.ctime(td3)   
print td3
print time.ctime(td4)   
print td4
print time.ctime(td5)   
print td5
print time.ctime(td6)   
print td6