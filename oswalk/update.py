#!/usr/bin/env python
import sys
import os
import fnmatch
import shutil
import xml.dom.minidom as Dom
import hashlib
converter = "/nfs/socv/data/tools/gpu/pdump2/linux64/Pdump2ToBinaryLite"
gpu_resource_dir = "/nfs/bonnie"
pdump2_script = "out2.txt"
static_image = "out2.prm"
target_file = "out2.txt.gz"
system_cfg_file = "/nfs/socv/data/gpu/bonnie/system.config"
bin_lite_file_name = "binliteplayer.bin"
working_dir = "/nfs/socv/data/"
case_temp_dir = "working"
hash_file_name = "hash_file.xml"

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
 
def calc_sha1(filepath):
    with open(filepath,'rb') as f:
        sha1obj = hashlib.sha1()
        sha1obj.update(f.read())
        hash = sha1obj.hexdigest()
        print(hash)
        return hash
def calc_sha256(filepath):
    with open(filepath,'rb') as f:
        sha1obj = hashlib.sha256()
        sha1obj.update(f.read())
        hash = sha1obj.hexdigest()
        print(hash)
        return hash
 
def calc_md5(filepath):
    with open(filepath,'rb') as f:
        md5obj = hashlib.md5()
        md5obj.update(f.read())
        hash = md5obj.hexdigest()
#         print(hash)
        return hash
    
def update_binliteplayer_data(src_dir):
    if ( os.path.isdir(src_dir) == False ) :
        print "convert dir is not exist"
        exit(-1)
    print "convert dir %s" %(src_dir)
    cmd = "%s -usesabs -c %s -a 0 %s -o %s" %(converter,system_cfg_file,"out2",src_dir+"/"+bin_lite_file_name)
    print cmd
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
    curdir = os.getcwd()
    fd = open(curdir+"/case_list.list","w")
    fd.writelines(items)
    fd.close
    
def read_template_xml(file_path):
    pass

def create_folder(dir):
    print dir
    os.makedirs(dir)
def create_output_dir(dir):
    os.makedirs(dir)

def gen_data_hash(file_path):
    pass
def gen_hash_xml(file_path,hash_data):
    doc = Dom.Document()  
    root_node = doc.createElement("root")  
    doc.appendChild(root_node)  
    
    input_node = doc.createElement("origin")
    root_node.appendChild(input_node) 
    for item in hash_data :
        id_node = doc.createElement("file")
        attr = id_node.setAttribute("name", item[0])
        id_value = doc.createTextNode(item[1])
        id_node.appendChild(id_value)
        input_node.appendChild(id_node) 
            
    print doc.toprettyxml(encoding="UTF-8")
    fd = open(file_path,"w")
    doc.writexml(writer=fd, indent="\n", addindent="\t", newl="", encoding="utf-8")


def print_brife_msg():
    print "flag file -> %s"%target_file
    print "bonnie memory module -> %s"  %system_cfg_file
def gen_origin_file_hash(subdir):
    print subdir
    hash_table = []
    
    for item in os.listdir(subdir) :
        tmp_hash = [1,2]
        if os.path.isdir(subdir + item) == True :
            print "skip dir -> %s" %(subdir + item)
            continue         
        tmp_hash[0] = item
        tmp_hash[1] = calc_md5(subdir+item)
        hash_table.append(tmp_hash)      
    print hash_table
    if os.path.isdir(subdir+case_temp_dir) == False :
        create_folder(subdir+case_temp_dir)   
    gen_hash_xml(subdir+case_temp_dir+"/"+hash_file_name,hash_table) 
def pre_gpu_test_case(subdir):
    cmd = "/bin/gzip -dfk %s/%s"%(subdir,"out2.txt.gz") 
    print cmd
    os.system(cmd)
    cmd = "/bin/gzip -dfk %s/%s"%(subdir,"out2.prm.gz") 
    print cmd
    os.system(cmd)
def post_gpu_test_case(subdir):
    pass
def init_gpu_test_case():
    all_dirs  = all_files(working_dir,target_file)
    for subdir in all_dirs :
        subdir = subdir.replace(target_file,"")
        update_binliteplayer_data(subdir)
        pre_gpu_test_case(subdir)
        gen_origin_file_hash(subdir)

        break
            
                
    


if __name__ == "__main__" :

#     working_dir = os.getcwd()
    print_brife_msg()
    init_gpu_test_case()
#     file_list = [ [ 'file1','hash1'],[ 'file2','hash2'],[ 'file3','hash3'],[ 'file14','hash4'] ]
#     gen_hash_xml("test",file_list)
    exit(0)
    argc = len(sys.argv)
    curdir = os.getcwd()
    
    print curdir
    if argc != 2:
        print help

        exit(0)
    if sys.argv[1] == "all" :
        update_all_subdir(curdir,target_file)
    elif sys.argv[1] == "list" :
        print "update list file"
        update_gpu_list_file(curdir,target_file)
        pass
    elif os.path.isdir(curdir+sys.argv[1]) :
        update_binliteplayer_data(curdir+sys.argv[1])
    else :
        print help
        
    
        
        