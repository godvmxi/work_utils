import sqlite3
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

INIT_CONFIG_VALUE = [                            
                        ['mode4','auto'],
                        ['mode6','auto'],                                    
                        ['ip4','222'],
                        ['ip6','333'],
                        ['via4','444'],
                        ['via6','555'],
                        
                        ['dns4',''],
                        ['dns6','']
                            ]
class test:
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
    def syncdata(self,src_object,des_object,if_temporary):
        print src_object
        print des_object
        print if_temporary
        if if_temporary :
            conn = sqlite3.connect(CPGMgt_ConfigDB.TEMP_CONFIG_DB)
        else :
            conn = sqlite3.connect(CPGMgt_ConfigDB.LOCAL_CONFIG_DB)
        c = conn.cursor()
        reply = ""        
        
        command = "SELECT key,default_value,value FROM start_config WHERE object = ?"
        print c.execute(command, [src_object])
        src = c.fetchall()
        print "sql result -->  ",
        print src
        for item in src :
            command = "UPDATE start_config Set default_value=? AND value=?  WHERE object=? and key=?"
            c.execute(command,[item[1],item[2],des_object,item[0]])
        print len(reply)
        conn.commit()
        conn.close()
        
        
object_name2= "/com/cisco/cpg/test3"
object_src= "/com/cisco/cpg/test3"
object_des= "/com/cisco/cpg/network/wired"



db =  test()
print db.firstInit( object_name=object_src,init_list=INIT_CONFIG_VALUE)
db.syncdata(object_src, object_des, False)

