# -*- coding: cp936 -*-
import win32com.client
from ctypes import *
import time
dmdll=win32com.client.Dispatch('dm.dmsoft')
print dmdll.GetDmCount()
print dmdll.Ver()
handler =  dmdll.FindWindow("","网络客户端")
print handler
print "try bind->",
#print dmdll.BindWindow(handler,"dx2","dx2","dx",0)
#dmdll.SetWindowState(handler,1)
#print dmdll.BindWindow(handler,"normal","windows","windows",0)
#print dmdll.BindWindow(handler,"normal","windows","dx",0)

dmdll.SetWindowState(handler,1)

def inputString(dmdll,x,y,text):
    #undo
    #sellect all
    #paste
    dmdll.SetClipboard(text)
    dmdll.MoveTo(x,y)
    dmdll.LeftClick()
    dmdll.RightClick()
    time.sleep(0.1)
    dmdll.MoveTo(x+30,y+75)
    dmdll.LeftClick()
    
    
    
    
#print dmdll.SendString(handler,"hello")
#print dmdll.SetWindowTransparent(handler,255)
print "isbind->",
print dmdll.IsBind(handler)
print "move to input one",
print dmdll.MoveTo(600,325)
#print dmdll.MoveTo(650,395)
#print dmdll.MoveTo(150,290)
print dmdll.SetClipboard("1111111")
print dmdll.GetClipboard()
print dmdll.LeftClick()

inputString(dmdll,600,325,"5645645")
inputString(dmdll,600,390,"234")

 
 
x=c_int(0)
y=c_int(0)
print "try get windown x ,y"
p = dmdll.GetPointWindow()
print x
print y
print p




print dmdll.UnBindWindow()

