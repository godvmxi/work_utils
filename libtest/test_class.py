class A():
    def __init__(self,a=None,b=None,c=None,):
        print 'A init'
        
        print "a-> %s"%a
        print "b-> %s"%b
        print "c-> %s"%c
        pass
class B():
    def __init__(self,path=None,**kwarg):
        print "B init"
        print "path-> %s"%path
        print "kwarg-> %s"%kwarg
        pass
class C():
    def __init__(self):
        print "C init"
class D():
    def __init__(self):
        print "D init"