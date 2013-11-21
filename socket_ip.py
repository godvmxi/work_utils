import socket 
import fcntl 
import struct 
import os
def __get_ip4():
        ip = os.popen(''' /sbin/ifconfig eth0 | grep 'inet addr'|awk '{print $2 $4}'  ''').readlines()
        result = []
        if len (ip) > 0 :
            ipmask = ip[0].split('M')

            if len(ipmask ) == 2 :
                ip = ipmask[0].split(':')[1]
                mask = ipmask[1].split(':')[1]
                result.append(   ip +'/'+ mask )
        out = ','.join(result)
        return out
 
def get_ip_address(ifname): 
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    return socket.inet_ntoa(fcntl.ioctl( 
        s.fileno(), 
        0x8915,  # SIOCGIFADDR 
        struct.pack('256s', ifname[:15]) 
    )[20:24]) 
 

#print "br0 = "+ get_ip_address('br0') 
#print "lo = " + get_ip_address('lo') 
#print "p32p1 = "+ get_ip_address('p2p1') 
#print "p32p1 = "+ get_ip_address('p8p1') 
#print "p32p1 = "+ get_ip_address('eth0') 
from IPy import IP
def getBrocastFromIpMask(ip,mask):
    ipmask = ip+'/'+mask
    return IP(ipmask,make_net=True).broadcast()

        

if __name__ == "__main__": 
#    ipmask = __get_ip4()
#    ip,mask =  ipmask.split('/')
#    
#    a = IP(ipmask,make_net=True)
#    print a.broadcast()
    print IP('192.168.1.1/255.255.255.0',make_net=True).broadcast()
    print IP('192.168.1.1/24',make_net=True).broadcast()

    