#!/bin/env python
a= ''

try :
    b=a
    print 'normal'
except :
    print 'except1'
    raise 'hello'
    print 'except2'
finally:
    print 'final'