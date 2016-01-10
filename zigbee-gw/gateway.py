#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
__author__ = 'Bright Jiang'

from cmd_define import *
from  config_utils import *
import signal

import threading
import cmd_utils

from serial_controller import *
import threading
from cmd_utils import  *
from http_utils import *

def  mainLoop():

    # 1:get -> json ->struct ->
    serial_handler = SerialUtils()
    serial_handler.open()
    local_http_handler = HttpUtils()
    parse_handler = CmdUtils()
    parse_handler.localNetStatus = False
    parse_handler.remoteNetStatus = True
    netHandler  ={
        "localPost":None ,
        "localGet":None   ,
        "remotePost":local_http_handler ,
        "remoteGet":local_http_handler,
        "serial" :serial_handler
    }
    print serial_handler
    parse_handler.setHandler(netHandler)

    thread_dict = {}
    thread_dict["serial_write"]  = threading.Thread(target=serial_handler.writeLoop )

    thread_dict["serial_read"]   = threading.Thread(target=serial_handler.readLoop)



    thread_dict["data_parse"]   = threading.Thread(target=parse_handler.readSerialSerialQueue)

    thread_dict["remote_post"]  = threading.Thread(target=parse_handler.readPostRemoteLoop)
    # thread_dict["server_get"]   = threading.Thread(target=parse_handler.getRemoteWriteLoop)
    # thread_dict["net_status"] =  threading.Thread(target=local_http_handler.check)



    for key in thread_dict.keys() :

        thread_dict[key].setDaemon(True)
        thread_dict[key].start()

    while True :
        time.sleep(2)

    print "thread start over"

    print thread_dict

def load_config_from_file(config_file):
    pass

if __name__  ==  "__main__" :
    # parser = OptionParser()
    # parser.add_option("-c", "--config", action="store_true",
    #                 dest="config",
    #                 default=None,
    #                 help="cmd type")
    # parser.add_option("-t", "--requsetType", action="store_true",
    #                 dest="requsetType",
    #                 default='get',
    #                 help="http request type,just support get & post")
    # parser.add_option("-s", "--server", action="store_true",
    #                 dest="server",
    #                 default='http://127.0.0.1',
    #                 help="http host name")
    # (options, args) = parser.parse_args()
    # signal.signal(signal.SIGINT, handler)
    # signal.signal(signal.SIGTERM, handler)
    try :
        mainLoop()
    except KeyboardInterrupt:
        import sys
        sys.exit()


