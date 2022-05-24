#!/usr/bin/env   python2.7 
import os
import json
import pprint
query_cmd = "ssh -p 29418 bright.jiang@gerrit.in.infotm.com  gerrit query  --format=JSON  --all-approvals status:open"

def get_commit_id_list (cmd ):
    buf = os.popen(cmd).readlines()
    commit_list = []
    index = 0
    for line in buf :
        temp = json.loads(line)
        try :
            if temp["owner"]['username']  == u'bright.jiang'  and temp['subject'] == 'commit test' :
                commit_id =  temp['patchSets'][0]["revision"]
                commit_list.append([commit_id,temp['url']])
                index = index +1 
            #pprint.pprint((  commit_id ,temp["url"] ))
        except :
            print("error -> %s"%temp)

    print("total changes -> %s"%len(commit_list))
    return commit_list[:25]
def abandon_commit_id(id_list):
    for id in id_list :
        cmd = "ssh -p 29418 bright.jiang@gerrit.in.infotm.com    gerrit review --abandon   %s" %id[0]
        result = os.system(cmd)
        print("abandon  %s  %s"%(id[1],result))
id_list = get_commit_id_list(query_cmd)
abandon_commit_id(id_list)
