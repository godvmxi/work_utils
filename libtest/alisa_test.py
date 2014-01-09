#!/bin/env python
import importlib
    
def foo(*args, **kwargs):
    print 'args = ', args
    print 'kwargs = ', kwargs
    print '---------------------------------------'
    
    
class subs():
    def __init__(self):
        pass
    def add(self,name,**kwarg):
        module = importlib.import_module('test_class')
#        print module
        print 'input para',
        print kwarg
        arg = str( kwarg)
        print arg
        attr =  getattr(module, name)
        return attr(a='a?dhsfkahds',**kwarg)



if __name__ == '__main__':
    sub = subs()
    sub.add( "A", c='sdsd',b='ttttdsfa' )
#    sub.add("B")
#    sub.add("C")
    
    exit()
    foo(1,2,3,4)
    foo(a=1,b=2,c=3)
    foo(1,2,3,4, a=1,b=2,c=3)
    foo('a', 1, None, a=1, b='2', c=3)
#if __name__ == "__main__":
#    a = subs('hello',('hello2','name'))