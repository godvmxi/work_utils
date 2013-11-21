import sqlite3
from cpgmgt_service_object import CPGMgt_Service_Object
#from _threading_local import key
__CPGMGT_HOME = "/usr/lib/python2.7/site-packages/cpgmgt-service/"
__LOCAL_CONFIG_DB_PATH = __CPGMGT_HOME + "share/config-database/"
__TEMP_CONFIG_DB_PATH = "/run/cpgmgt-service/"
__CONFIG_DB_NAME = "cpgmgt_config.db"

LOCAL_CONFIG_DB = __LOCAL_CONFIG_DB_PATH + __CONFIG_DB_NAME   
TEMP_CONFIG_DB = __TEMP_CONFIG_DB_PATH + __CONFIG_DB_NAME
#
#conn = sqlite3.connect(TEMP_CONFIG_DB)
#c = conn.cursor()
#reply = ""
#
#
#command = "SELECT key,value FROM start_config WHERE object = ?"
#print c.execute(command, ["/com/cisco/cpg/test"])
##command = "SELECT * FROM start_config "
##c.execute(command)
#reply = c.fetchall()
#print reply
#print len(reply)
#conn.commit()
#conn.close()


from cpgmgt_common import CPGMgt_ConfigDB


class test:
    INIT_CONFIG_VALUE = [                            
                        ['mode4','auto'],
                        ['mode6','auto'],                                    
                        ['ip4',''],
                        ['ip6',''],
                        ['via4',''],
                        ['via6',''],                        
                        ['dns4',''],
                        ['dns6','']
                            ]
    def __init__(self):
        print "test init"
        pass
    

    def firstInit(self,if_temp=True,object_name="",init_list=[]):
        if if_temp :
            db = CPGMgt_ConfigDB.TEMP_CONFIG_DB
        else :
            db = CPGMgt_ConfigDB.LOCAL_CONFIG_DB
        result =  CPGMgt_ConfigDB.get_value_of_database(
            object_name, key=None, value_type="value", db_file=db)
        print "init date result -->",
        print result
        if len(result) == len(init_list):
            #donothing 
            return "not first init"
        for key_value_item in init_list:                
            key_name = CPGMgt_ConfigDB.convert_to_str(key_value_item[0])
            value = CPGMgt_ConfigDB.convert_to_str(key_value_item[1])
            CPGMgt_ConfigDB.insert_data_to_database( object_name, 
                key_name, value, 
                None, True, CPGMgt_ConfigDB.TEMP_CONFIG_DB)
        return "first init"
    @staticmethod
    def syncdata(main_object="",child_object="",if_temporary=True,syncDirect=True,init_table=[]):
        print main_object
        print child_object
        print if_temporary
        if if_temporary :
            conn = sqlite3.connect(CPGMgt_ConfigDB.TEMP_CONFIG_DB)
            print "use temp db"
        else :
            conn = sqlite3.connect(CPGMgt_ConfigDB.LOCAL_CONFIG_DB)
        
        
        if syncDirect :
            #copy data from main store 
            copy_src = main_object            
            copy_des = child_object

        else :
            #make current data to main store
            copy_src = child_object            
            copy_des = main_object

        c = conn.cursor()
        command = "SELECT key,default_value,value FROM start_config WHERE object = ?"
        c.execute(command, [copy_src])
        src = c.fetchall()

        
        
        print "sql src -->  ",
        print src
        for item in src :
            key =   str ( item[0] )
            if key in init_table:
                default_value = str(item[1])
                value =  str(item[2])            
                
                command = "UPDATE start_config SET default_value = ? , value = ? WHERE object = ? AND key = ?"
                c.execute(command,[ default_value ,value,copy_des,key])
                print c.rowcount,
                print " --> ",
                print item
            else :
                print "key not in main table ,not sync->" +key
            
        command = "SELECT key,default_value,value FROM start_config WHERE object = ?"
        c.execute(command, [copy_des])
        src = c.fetchall()
        print "sql dest -->  ",
        print src
        conn.commit()
        conn.close()

    def getKeyList(self):
        result =[]
        for key_value_item in self.INIT_CONFIG_VALUE:
                result.append(key_value_item[0])
        print "keylist--> ",
        print result
        return result
        
object_name2= "/com/cisco/cpg/test3"
object_des= "/com/cisco/cpg/test"
object_src= "/com/cisco/cpg/network/wired"


import sys
direct=True

if len(sys.argv) >1:
    direct = False
db =  test()
keys=db.getKeyList()
#print db.firstInit( object_name=object_src,init_list=db.INIT_CONFIG_VALUE)
#db.syncdata(main_object="object_src", child_object="object_des",if_temporary=True,syncDirect=False,init_table=db.getKeyList())
print object_src
print object_des
print keys
db.syncdata(object_src,object_des,True,direct,keys)






#db.syncdata(main_object=object_src, child_object=object_des, if_temporary=True,syncDirect=False)

