import sys
import inspect
def fool():
    pass
class Cat(object):
    def __init__(self,name='kitty'):
        self.name = name
    def sayHi(self):
#        print self.name ,' : say Hi'
        print '%s : say Hi' %(self.name)

cat = Cat()
print ".."
print cat.sayHi()
print "??"
print Cat.sayHi