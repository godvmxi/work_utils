__author__ = 'bluebird'

from cpgmgt_common.cpgmgt_configdb import  *


db = CPGMgt_ConfigDB()
object_path = "/com/cisco/cpg/Network/NonWiFi/NameServer"
key=None
source_db=CPGMgt_ConfigDB.TEMP_CONFIG_DB
target_db=CPGMgt_ConfigDB.LOCAL_CONFIG_DB
CPGMgt_ConfigDB.import_database_from_file(source_db,object_path, key, target_db)
print 'sync over'