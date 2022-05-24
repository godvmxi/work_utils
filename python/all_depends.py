#!/bin/bash
import os
devel_rpm_list = []
runtime_rpm_list = []
installed_list = []
def install_rpm(type,rpm):
    print "will install the rpm to list"
    #do some thing to install it
    if type == "devel" :        
        os.system("rpm -ivh ")
    elif type == "run" :
        os.system("rpm -ivh ")
    else :
        print "error"
        raise "fault error ,not exist"
    installed_list.append(rpm)
    return 
def getDependList(srpm):
    print "return two list ,one running list and one devel list"
    return [["running_list"],["devel_list"]]
def getNextDependChild(srpm):
    depend_list = getDependList(srpm)
    runtime_depends = depend_list[0]
    devel_depends = depend_list[1]
    for item in runtime_depends : #check whether tht lis is ready
        if item in runtime_rpm_list :
            print "current item in devel_list -> %s "%(srpm)            
        else :
            print "item is not exist -> %s " %(srpm)
            return ["devel",item]
    for item in devel_depends :#devel list
        if item in devel_rpm_list :
            print "current itme in running_list -> %s" %(srpm)
        else :
            print "item is not exist -> %s " %(srpm)
            return ["run",None]
    return [None,None] #没有依赖
def buildAndLogResult(srpm):    
    os.system("rpmbuild --rebuild %s " %(srpm))
    #log the result rpms
    return "result"
def dealSrpm(srpm):
    depend  = getNextDependChild(srpm)
    if depend  == [None,None] :
        print "reach the bottom and rebuild it"
        buildAndLogResult(depend[0],srpm)
        install_rpm[depend[0],srpm]
        
        return 
    else :
        dealSrpm(srpm)

        
        
        
        
        
        
            
    