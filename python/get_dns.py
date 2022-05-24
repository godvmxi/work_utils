__author__ = 'bluebird'
import os
import pprint

def get_all_dns():
        lines = os.popen('nm-tool ').readlines()
        result = {}
        tmpkey = ''
        for line in lines :
            if line.find("Device:") > 0:
                keys = line.split()
                tmpdev = keys[2]
                result[tmpdev]  = []
            else :
                if line.find('DNS') > 0:

                    line = line.split()
                    result[tmpdev].append(line[1])

        return result
if __name__ == '__main__' :
    print get_interface_dns()
