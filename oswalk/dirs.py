
import os, fnmatch

rename_list = ["out.3dsig.bin","out.hwperf.bin","out.tasig.bin","out.trace.bin","outfb0.bin","outfb0.bmp","outfb0_diff_thumb.png","outfb0_thumb.png"]
untar_list = ["out2.txt.gz","out2.prm.gz"]
copy_list = ["out2.txt","out2.prm"]

all_dirs = []
less_dirs = []


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
def sort_dir():
    pass
def create_dir_name(filepath):
    dirname = ""
    if filepath.find("Integration")  > 0 :
        dirname += "integration-"
    elif filepath.find("Compatibility") :
        dirname += "compatibility-"
    else:
        raise Exception("wrong suites")
    newpath = filepath.split("/")[1:-1]
    dirname +=  "-".join(newpath)
#     print dirname
    return dirname
    
def copy_to_new_dir(oldpath,newpath):
    
    oldpath = oldpath.replace("out2.txt.gz","")
    print "copy : %s --> %s" %(oldpath,newpath)
    cmd =  "cp -rf %s  %s" %(oldpath,newpath)
    os.system(cmd)
def untar_file_in_new_dir(file):
    cmd = "gzip -dfk %s " %(file)
    os.system(cmd)
def create_new_dir(newdir):
    cmd = "mkdir -p %s" %(newdir)
    os.system(cmd)
def copy_file_list(src_dir,des_dir,gz_file_list):
    for gzfile in gz_file_list:
        temp  = all_files(src_dir,gzfile)
        index = 0
        for path in temp:
                index += 1
                print "%s -> %s  ->%s"%( index ,path,des_dir)
                tmp_dest_dir = path.replace(src_dir,des_dir)
                cmd = "cp -rfv %s %s" %(path,tmp_dest_dir)
                print cmd
#                 os.system(cmd)

def copy_rename_file_list(src_dir,des_dir,gz_file_list,prefix):
    for gzfile in gz_file_list:
        temp  = all_files(src_dir,gzfile)
        index = 0
        for path in temp:
                index += 1
                print "%s -> %s  ->%s"%( index ,path,des_dir)
                
                filename = path.split("/")[-1]
                newfilename = prefix+filename
                tmp_dest_dir = path.replace(src_dir,des_dir)
                tmp_dest_dir = tmp_dest_dir.replace(gzfile,newfilename)
                
                cmd = "cp -rfv %s %s" %(path,tmp_dest_dir)
                print cmd
#                 os.system(cmd)




def untar_file_list(src_dir,des_dir,gz_file_list):
    for gzfile in gz_file_list:
        temp  = all_files(src_dir,gzfile)
        index = 0
        for path in temp:
            index += 1
            print "%s -> %s"%( index ,path)
            temppath = path.replace(gzfile,"")
            newpath = temppath.replace(dir_home,target_home)
            
def diff_dirs(src_dir):
    all_file = "out2.txt"
    
    for less_file in rename_list:
        temp  = all_files(src_dir,all_file)
        all_dirs = []
        less_dirs = []
        for path in temp :
            
            all_dirs.append(path.replace(all_file,""))
        temp  = all_files(src_dir,less_file)
        
        for path in temp :
            less_dirs.append(path)
            all_dirs.remove(path.replace(less_file,""))
        print "current item -> %s" %(less_file)
        index= 0
        for dir in all_dirs :
            index +=1
            print "%s --> %s"%(index,dir)
        
    

if __name__ == '__main__':
    dir_home = '/home/dan/ownCloud/Multimedia/GPU/new/GPU/GPU'
    target_home = '/home/dan/ownCloud/Multimedia/GPU/new/GPU/GPU2'
    temppath = ""
    diff_dirs(dir_home)
#     copy_file_list(dir_home,target_home,copy_list)
#     copy_rename_file_list(dir_home,target_home,rename_list,"std_")
    
    



