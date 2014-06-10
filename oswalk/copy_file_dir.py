import os


list_table = [[0,49],[50,99],[100,149],[150,199]]
def open_file_list(file,index):
    pass

if __name__ == "__main__":
    index = 0
    target_home = "/nfs/socv/data/gpu/bonnie/comp_test"
    filelist = open("/nfs/bonnie/comp_test/case_list.list","r").readlines()
    newfllelist = filelist[list_table[index][0]:list_table[index][1]+1]
    print len(newfllelist)
    for file in newfllelist :
        file = file.replace("\n","")
        src_path = "/nfs/bonnie/comp_test/%s"%(file)
        des_path = "%s/%s"%(target_home,file)
        print " %s  -> %s"%(src_path,des_path)
        cmd = "cp -rfv %s  %s" %(src_path,des_path)
        print "cmd -> %s"%cmd 
#         os.system(cmd)
    print "copy over!!!!!!!!!!!!"