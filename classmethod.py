class A():
    def __init__(self):
        self.a = 0
    def hello(self):
        self.a = self.a +1
        print "hello A  -> %s" %(self.a)
class B():
    def __init__(self,handle):
        self.tmp = handle
        self.tmp.hello()


        
a = A()
b = B(a)
B(a)
B(a)
B(a)
B(a)


