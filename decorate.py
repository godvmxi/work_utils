from cpgmgt_common.cpgmgt_configdb import *
def cpgmgt_net_init(f):
    def init(self, bus = None, object_path = None, parent_path = None):
        self.cpgmgt_log.debug('Initializing {}'.format(self.__class__))

        self.bus = bus
        self.object_path = object_path
        self.parent_path = parent_path

        self.InitConfig(if_recover = "False", if_temporary = "False")

        self.sub_objs = None
        f(self)
        
        
    return init


def decorate_test(f):
    def init(self):
        print "fuck you before"
        f(self)
        print "fuck you later"
        print self.i
        print self.init_table
    return init
        
class A():
    init_table = 'hello'
    @decorate_test
    def __init__(self):
        self.i = 00000
        print "I am in class"
        
if __name__ == "__main__":
    db = CPGMgt_ConfigDB()
    object_path = '/com/cisco/cpg/Network/WiFiAP/ApIpconf'
    dat_list = db.get_data_list_of_database(object_name=object_path,  value_type='all', db_file=db.LOCAL_CONFIG_DB)
    print dat_list
    db.insert_data_list_to_database(data_list=dat_list, if_replace=True, db_file=db.TEMP_CONFIG_DB)
    dat_list = db.get_data_list_of_database(object_name=object_path,  value_type='all', db_file=db.TEMP_CONFIG_DB)
    print dat_list
