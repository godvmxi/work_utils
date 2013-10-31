class A:
    def __init__(self):
        print "A"
    def hello(self):
        print "A hello"
class B:
    def __init__(self):
        print "B"
    def hello(self):
        print "B hello"
class C:
    def __init__(self):
        print "C"
    def hello(self):
        print "C hello"
class D(C) :
    def hello(self):
        print "D hello"