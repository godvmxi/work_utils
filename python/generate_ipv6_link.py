__author__ = 'bluebird'
import os

class IPv6_link(object):
    def __init__(self,iface):
        self.iface =iface
        pass
    @staticmethod
    def get_iface_mac(iface=None) :

        cmd = "/sbin/ifconfig %s |grep HWaddr|awk '{print $5}'"%(iface)
        buf = os.popen(cmd).read()
        mac = buf.replace('\n','').replace(' ','')

        return mac

    @staticmethod
    def generate_ipv6_link(mac=None):

        mac_str = mac.replace(':','')
        if len(mac_str) !=  12 :
            raise Exception("mac address error")
        tmp = mac_str[0:6] +'FFFE' +mac_str[6:]
        mac_str = tmp
        byte2 = mac_str[1]
        byte2 = int(byte2,16)
        byte2 = byte2 ^0x02
        byte2 = '%X'%(byte2)
        tmp_str = mac_str[0] + byte2[0] +mac_str[2:]
        result =  'FE80' + tmp_str
        link = result[0:4] + "::" +result[4:8] + ":" +result[8:12] + ":" \
               +result[12:16] + ":" +result[16:]
        return link

    @staticmethod
    def get_iface_ipv6_link(iface) :
        cmd = "/sbin/ifconfig %s |grep Scope:Link | awk '{print $3}'"%(iface)
        buf = os.popen(cmd).read()
        if len(buf)  <=  4:
            raise Exception('no ip link address')
        link = buf.replace('\n','').replace(' ','')
        return link.upper()
    @staticmethod
    def add_iface_ipv6_link(iface,link_local):
        cmd  = 'ifconfig %s inet6 add %s/64' %(iface,link_local)
        os.system(cmd)




if __name__ == "__main__" :



    mac = IPv6_link.get_mac('p8p1')
    print mac
    link =  IPv6_link.generate_ipv6_link(mac)
    print 'Link-->',
    print link.lower()
    IPv6_link.add_iface_ipv6_link('p8p1',link)








'''
08:00:27:87:78:33

fe80::a00:27ff:fe87:7833
'''