#!/usr/bin/env python
import sys
import os
import fnmatch
import shutil
converter = "/var/ASIC_ICVERIFY_DATA/tools/GPU/pdump2/linux/64bit/Pdump2ToBinaryLite"
gpu_resource_dir = "/nfs/bon"
pdump2_script = "out2.txt"
static_image = "out2.prm"
target_file = pdump2_script
system_cfg_file = "system.config"
bin_lite_file_name = "binliteplayer.bin"

help='''
para :
    all :update all subdirs 
    subdir :update target dir ,must be valid
    list : update the subdir list

'''
folder_list = [ "","","","",""]
def all_files(root, patterns = '*', single_level = False, yield_folders=False):
    patterns = patterns.split(';')
    for path, subdirs, files in os.walk(root):
        if yield_folders:
            files.extend(subdirs)
        files.sort()
        for name in files:
            for pattern in patterns:
                if fnmatch.fnmatch(name, pattern):
                    yield os.path.join(path,name)
                    break
        if single_level:
            break
def update_binliteplayer_data(src_dir):
    if ( os.path.isdir(src_dir) == False ) :
        print "convert dir is not exist"
        exit(-1)
    print "convert dir %s" %(src_dir)
    cmd = "%s -c %s -a 0 %s -o %s" %(converter,gpu_resource_dir+system_cfg_file,"out2",src_dir+"/"+bin_lite_file_name)
    os.system(cmd)
    cmd = "mv %s %s" %(bin_lite_file_name,src_dir)
def update_all_subdir(src_dir,find_file):

    all_dirs  = all_files(src_dir,find_file)
    for subdir in all_dirs :
        subdir = subdir.replace(find_file,"")
        update_binliteplayer_data(subdir)
        
def update_gpu_list_file(src_dir,find_file):
    all_dirs  = all_files(src_dir,find_file)
    items = []
    for subdir in all_dirs :
        subdir = subdir.split("/")[-2] + "\n"
        items.append(subdir)
    print "update items -> %d" %(len(items))
    fd = open(gpu_resource_dir+"case_list.list","w")
    fd.writelines(items)
    fd.close
    
        
def create_folder(dir):
    pass


if __name__ == "__main__" :
    
    argc = len(sys.argv)

    if argc != 2:
        print help
        exit(0)
    if sys.argv[1] == "all" :
        update_all_subdir(gpu_resource_dir,target_file)
    elif sys.argv[1] == "list" :
        print "update list file"
        update_gpu_list_file(gpu_resource_dir,target_file)
        pass
    elif os.path.isdir(gpu_resource_dir+sys.argv[1]) :
        update_binliteplayer_data(gpu_resource_dir+sys.argv[1])
    else :
        print help
        
    
        
        