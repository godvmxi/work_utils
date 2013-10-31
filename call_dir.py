#!/usr/bin/env python
import os
import subprocess
main = '/etc/netlink/'
wired_link_up = 'wired_link_up'
wired_addr_ready = 'wired_addr_ready'

def run_dir(path):
    ls = os.listdir(path)
    for tmp in ls :
        print tmp
        tmp = path+'/'+tmp
        cmd = '/bin/bash %s  &' %(tmp)
        print cmd
        print 
        os.system(cmd)
    
    

if __name__ == '__main__':
    run_dir(main+wired_addr_ready)