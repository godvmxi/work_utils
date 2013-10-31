#!/usr/bin/env python
import dbus
import os
import time
import subprocess


NM_IFNAME_NETWORKMANAGER = "org.freedesktop.NetworkManager"
NM_IFNAME_PROPERTIES = "org.freedesktop.DBus.Properties"
NM_IFNAME_ACCESSPOINT = "%s.%s" % (NM_IFNAME_NETWORKMANAGER, "AccessPoint")
NM_IFNAME_DEVICE = "%s.%s" % (NM_IFNAME_NETWORKMANAGER, "Device")
NM_IFNAME_WIRELESS = "%s.%s" % (NM_IFNAME_NETWORKMANAGER, "Device.Wireless")
NM_IFNAME_SETTINGS = "%s.%s" % (NM_IFNAME_NETWORKMANAGER, "Settings")
NM_IFNAME_CONNECTION = "%s.%s" % (NM_IFNAME_NETWORKMANAGER, "Settings.Connection")
NM_IFNAME_CONACTIVE = "%s.%s" % (NM_IFNAME_NETWORKMANAGER, "Connection.Active")
NM_IFNAME_IP4CONFIG = "%s.%s" % (NM_IFNAME_NETWORKMANAGER, "IP4Config")
NM_IFNAME_IP6CONFIG = "%s.%s" % (NM_IFNAME_NETWORKMANAGER, "IP6Config")
NM_IFNAME_DHCP4CONFIG = "%s.%s" % (NM_IFNAME_NETWORKMANAGER, "DHCP4Config")
NM_IFNAME_DHCP6CONFIG = "%s.%s" % (NM_IFNAME_NETWORKMANAGER, "DHCP6Config")
NM_IFNAME_NETWORKMANAGER= "org.freedesktop.NetworkManager"


GE_PCI_ID = '0000:01:00.0'
def get_eth_ifname_by_pci(pci_id):
    ifdir = "/sys/bus/pci/devices/" + pci_id + "/net"
    if not os.path.isdir(ifdir):
        raise Exception("ERROR: Cannot find network interface by PCI ID: {}"\
                .format(pci_id))
    name = os.listdir(ifdir)
    return name[0]



def GetMethodInterfaceHandle(iface_name, iface_path = None):
    bus = dbus.SystemBus()
    if iface_name[0:1] != '.' and iface_name[0:1] != '/':
        iface_path_tmp = '/' + iface_name.replace('.', '/')
    else :
        iface_path_tmp = iface_name.replace('.', '/')

    # Get a proxy for the base NetworkManager object 
    proxy = bus.get_object(NM_IFNAME_NETWORKMANAGER, iface_path_tmp)
    if (iface_path != None) :
        iface = dbus.Interface(proxy, iface_path)
    else:
        iface = dbus.Interface(proxy, iface_name)

    return iface

def GetPropertyInterfaceHandle(iface_name):
    bus = dbus.SystemBus()
    if iface_name[0:1] != '.' and iface_name[0:1] != '/':
        iface_path_tmp = '/' + iface_name.replace('.', '/')
    else :
        iface_path_tmp = iface_name.replace('.', '/')

    proxy = bus.get_object(NM_IFNAME_NETWORKMANAGER, iface_path_tmp)
    iface = dbus.Interface(proxy, NM_IFNAME_PROPERTIES)
    return iface

def __get_interface_dev(interface):
    manager = GetMethodInterfaceHandle(NM_IFNAME_NETWORKMANAGER)
    devices =  manager.GetDevices()
    print 'interface dev -->%s ' %(interface)
    set_dev = None
    set_state = None
    print "get interface dev"
    for dev in devices :

        #    dev.Disconnect()
        
        prop_iface = GetPropertyInterfaceHandle(dev)

        iface =  prop_iface.Get(NM_IFNAME_DEVICE, "interface")
        print iface

        if iface == interface:
            set_dev = dev
            return [True,set_dev,manager]
    return [False,None,None]
def __get_mac_by_interface(interface):
    print "get mac fron %s" %(interface)
    cmd = "ifconfig "+interface +" |grep HWaddr"
    print cmd
    mac = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    mac = mac.communicate()[0]
    mac = mac.split()
    print mac
    
    if len(mac) == 5:
        print "fuck you"
        mac =  mac[4].split(':')
        print mac
        result = []
        for dat in mac:
            result.append(int(dat,16))
        print result
        return result 
    else :
        return None
def __get_interface_connection(interface):
    print 'interface conn -->%s ' %(interface)
    mac1 = __get_mac_by_interface(interface)
    print mac1
    settings_pros = GetMethodInterfaceHandle(NM_IFNAME_SETTINGS)
    print settings_pros
    settings = settings_pros.ListConnections()
    print "get interface connect"
    print settings
    for setting in settings :
        
        connect =  GetMethodInterfaceHandle(setting, NM_IFNAME_CONNECTION)
#        print "connect",
#        print connect
        allSetting =  connect.GetSettings()
#        print "allSetting",
#        print allSetting

        uuid = allSetting['connection']['uuid']
        mac2 = ""
        try :
            mac2 =  allSetting['802-3-ethernet']['mac-address']
        except :
            print "can't find mac2"
            mac2 = ''
        print mac2
        print 
        if mac2 == mac1 :
            print "find interface"
            return [True,setting]
    print "can't find interface"
    return [False,None]
def __try_reconnect_interface(interface):
    try :
        dev = __get_interface_dev(interface)
        con = __get_interface_connection(interface)
        print dev
        print con
        if dev[0] == True and con[0] == True:
            try :
                try :
                    iface = GetMethodInterfaceHandle(dev[1],NM_IFNAME_DEVICE)
                    iface.Disconnect()
                    print "disconnect\t->    %s"%(interface)
                except :
                        print "can,t disconnect"
                time.sleep(10)
                manager = dev[2]
                print "connect\t->    %s" %(interface)
                manager.ActivateConnection(con[1],dev[1],"/")
                
            except :
                print "device not alive"
                raise Exception("device not alive")
                
    except :
        print "restart NetworkMananger"


if __name__ == '__main__':
    print "start active"
    
    iface = 'p8p1'
    iface = get_eth_ifname_by_pci(GE_PCI_ID)
    
    __try_reconnect_interface(iface)
    exit()
    
    
    set_dev = ''
    manager = GetMethodInterfaceHandle(NM_IFNAME_NETWORKMANAGER)
    devices =  manager.GetDevices()
    for dev in devices :
        print "dev --> ",
        print dev
        #    dev.Disconnect()
        prop_iface = GetPropertyInterfaceHandle(dev)
        print prop_iface
        print "interface -> ",
        interface =  prop_iface.Get(NM_IFNAME_DEVICE, "interface")
        print interface
        print "state -> ",
        if interface == "p8p1":
            set_dev = dev
        print prop_iface.Get(NM_IFNAME_DEVICE, "state")
    

    iface = GetMethodInterfaceHandle(set_dev,NM_IFNAME_DEVICE)
    print iface
    print "stop interface p8p1"
    try :
        time.sleep(2)
        iface.Disconnect()
        time.sleep(3)
    except :
        print 'device not alive'
        time.sleep(3)
        
    

    settings_pros = GetMethodInterfaceHandle(NM_IFNAME_SETTINGS)
    print settings_pros
    settings = settings_pros.ListConnections()
    set_connection = ''
    for setting in settings :
        print setting

        connect =  GetMethodInterfaceHandle(setting, NM_IFNAME_CONNECTION)
        allSetting =  connect.GetSettings()
        print allSetting
        print allSetting['connection']
        uuid = allSetting['connection']['uuid']
        print uuid
        interface =  allSetting['connection']['id']
        if interface == "p8p1" :
            set_connection = setting

    print "set data -->  "
    print "dev"
    print set_dev
    print "connect"
    print set_connection
    
    print "start connect"
    manager.ActivateConnection(set_connection,set_dev,"/")

#    print settings_ifaces
#    settings = settings_ifaces.ListConnections()
#    print "2"
#    for setting in settings:
#        print setting.GetSetting()
    

    
