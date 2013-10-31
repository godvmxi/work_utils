#!/usr/bin/env python
from cpgmgt_service_object import CPGMgt_ConfigDB
from cpgmgt_service_object import *
class Get_Db(CPGMgt_Service_Object): 
    def __init__(self):   
        reply = self.getconfig(object_name = '/com/cisco/cpg/WiFiMode', key = 'mode', if_temporary = "True")
        print reply
def get_wifimode():
    from cpgmgt_service_object import CPGMgt_ConfigDB
    return CPGMgt_ConfigDB.get_value_of_database(object_name = '/com/cisco/cpg/WiFiMode', key = 'mode',db_file = CPGMgt_ConfigDB.TEMP_CONFIG_DB)
   
if __name__ == '__main__':
    print 'begin get data from db'
#    test = Get_Db()
    print get_wifimode()
    exit()