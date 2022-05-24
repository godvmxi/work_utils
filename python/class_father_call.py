class A(object):
    def help(self,msg):
        print 'a help  -> %s'%msg
class B(A):
    def help(self,msg):
        A.help(self,msg)
class C(A):
    def help(self,msg):
        super(C,self).help(msg)
bbb = B()
bbb.help('bbb')
ccc= C()
ccc.help('ccc')
