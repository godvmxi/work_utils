__author__ = 'bluebird'
import logging
import os
import sys
logger = logging.getLogger()
formatter = logging.Formatter('%(name)-12s %(asctime)s %(levelname)-8s %(message)s', '%a, %d %b %Y %H:%M:%S',)
file_handler = logging.StreamHandler()
file_handler.setFormatter(formatter)
stream_handler = logging.StreamHandler(sys.stderr)

logger.addHandler(stream_handler)

def is_valid_ipv4(dat):
    if dat == "" or dat =='::' :
        return False
    return True
class GatewaySwitch(object):
    def __init__(self):
        self.ge_iface = 'p32p1'
        self.ra_iface = 'ra0'
        pass
    staticmethod
    def check_gateway(self):
        '''
         set interface priority
        '''
        gws_origin =  os.popen('/usr/bin/nm-tool |grep Gateway').readlines()
        logger.info( gws_origin )
        gws = []
        for gw in gws_origin:
            dat = gw.split()
            if len(dat) != 2 :
                logger.error("gw split error")
                return
            else :
                if is_valid_ipv4(dat[1]) :
                    gws.append(dat[1])
                else :
                    print "ipv6 address,do nothing"
        if len(gws) != 2:
            print 'not ready to set prrority-->%s '%gws
            logger.info('not ready to set prrority')
            return
        devs = os.popen('/usr/bin/nm-tool |grep "Device:"').readlines()

        if  len(devs) < 2 :
            return
        else :
            print 'devs--> ',
            print devs[0]

            print 'gws--> ',
            print gws
            dev_1 = devs[0].split()
            dev_2 = devs[1].split()
            print dev_1
            print dev_2
            if dev_1[1] != 'Device:' or dev_2[1] != 'Device:':
                logger.info(  "device can match request" )
                return

            if dev_1[2] ==  self.ra_iface  and dev_2[2] == self.ge_iface :
                print 'self.ra_iface and p32p1'
                logger.info('self.ra_iface and p32p1')

                gateways =  os.popen(''' /sbin/route -n |grep UG |awk '{print $2}' ''').readlines()
                print gateways
                for gw in gateways :
                    gw = gw.strip()
                    if is_valid_ipv4(gw) :
                        del_gw = 'route del default gw %s' %(gw)
                        os.system(del_gw)
                cmd_add_high = '/sbin/route add default gw %s metric 3 %s' %(gws[0] ,dev_1[2])
                cmd_add_low = '/sbin/route add default gw %s metric 9 %s' %(gws[1] ,dev_2[2])
                print cmd_add_high
                print cmd_add_low
                logger.info(cmd_add_high)
                logger.info(cmd_add_low)
                os.system(cmd_add_high)
                os.system(cmd_add_low)
                return
            elif dev_1[2] == self.ge_iface and dev_2[2] == self.ra_iface :
                logger.info('p32p1 and self.ra_iface')
                print 'p32p1 and self.ra_iface'
                gateways =  os.popen(''' /sbin/route -n |grep UG |awk '{print $2}' ''').readlines()
                for gw in gateways :
                    gw = gw.strip()
                    print gw
                    if is_valid_ipv4(gw) :
                        del_gw = 'route del default gw %s' %(gw)
                        os.system(del_gw)
                cmd_add_high = '/sbin/route add default gw %s metric 3 %s' %(gws[1] ,dev_2[2])
                cmd_add_low  = '/sbin/route add default gw %s metric 9 %s' %(gws[2] ,dev_1[2])
                print cmd_add_high
                print cmd_add_low
                logger.info(cmd_add_high)
                logger.info(cmd_add_low)
                os.system(cmd_add_high)
                os.system(cmd_add_low)
                return
            else :
                logger.info("do nothing")
                return

if __name__ == "__main__" :
    gw =  GatewaySwitch()
    gw.check_gateway()