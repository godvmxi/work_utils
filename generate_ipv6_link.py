__author__ = 'bluebird'
import os

class IPv6_link(object):
    def __init__(self,iface):
        self.iface =iface
        pass
    @staticmethod
    def get_mac(iface=None) :

        cmd = "/sbin/ifconfig %s |grep HWaddr|awk '{print $5}'"%(iface)
        buf = os.popen(cmd).read()
        mac = buf.replace('\n','').replace(' ','')

        return mac
    @staticmethod
    def generate_ipv6_link(mac=None):

        # print self.mac
        mac_str = mac.replace(':','')
        if len(mac_str) !=  12 :
            raise Exception("mac address error")
        # print mac_str
        # print len(mac_str)
        tmp = mac_str[0:6] +'FFFE' +mac_str[6:]
        mac_str = tmp
        # print tmp
        # print len(tmp)
        byte2 = mac_str[1]
        # print byte2
        byte2 = int(byte2,16)
        byte2 = byte2 ^0x02
        byte2 = '%X'%(byte2)
        # print byte2
        # mac_str[1] = byte2[0]
        tmp_str = mac_str[0] + byte2[0] +mac_str[2:]
        # print tmp_str
        result =  'FF80' + tmp_str
        # print result
        # print len(result)
        link = result[0:4] + ":" +result[4:8] + ":" +result[8:12] + ":" \
               +result[12:16] + ":" +result[16:]
        return link



if __name__ == "__main__" :
    print 'I am here'
    link = IPv6_link("p8p1")
    mac = IPv6_link.get_mac('p8p1')
    print mac
    print link.generate_ipv6_link(mac)







'''
08:00:27:87:78:33

fe80::a00:27ff:fe87:7833
'''