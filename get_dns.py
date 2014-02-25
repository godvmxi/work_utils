__author__ = 'bluebird'
import os

def __get_interface_dns(iface):
        lines = os.popen('nm-tool ').readlines()
        result = []
        tmp = {}
        DNS = []
        dns_list = {}
        tmpkey = ''
        for line in lines :
            if line.find("Device:") > 0:
                dns_list.app
                keys = lines.split()
                tmpkey = tmpkey[2]
                if len(tmp) != 0:
                    tmp['dns'] = DNS
                    result.append(tmp)
                    tmp = {}
                    DNS = []

                line= line.split()
                tmp['dev'] = line[2]
            else :
                if line.find('DNS') > 0:

                    line = line.split()
                    DNS.append(line[1])

        tmp['dns']= DNS
        result.append(tmp)
    #    pprint.pprint(result)
        for tmp in result :
            if tmp['dev'] == iface:
                return tmp['dns']
        return []
if __name__ == '__main__' :
    print __get_interface_dns('p2p1')
    print "hello"
    print __get_interface_dns('p7p1')
    print "hello"
    print __get_interface_dns('p8p1')
    print "hello"
