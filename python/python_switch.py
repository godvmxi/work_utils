#def switch(value,x):
#    result = {
#      'a': lambda : x + 1,
#      'b': lambda : x + 2,
#      'c': lambda : x + 3
#                }
#    return result[value]()
#print swith('a',1)


def add(a,b):
    return a + b
def multi(a,b):
    return a* b
def sub(a,b):
    return a - b
def div(a,b):
    return a/ b#b is non-zero

def calc(type,x,y):
    calculation = {'+':lambda:add(x,y),
                   '*':lambda:multi(x,y),
                   '-':lambda:sub(x,y),
                   '/':lambda:div(x,y)}
    return calculation[type]()
#calc = {1:lambda:add(x,y)}[value]()

result1 = calc('+',3,6)
result2 = calc('-',3,6)
print result1, result2

ip="129.0.0.1/24"


