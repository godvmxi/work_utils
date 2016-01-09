#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
__author__ = 'Bright Jiang'

from cmd_define import *
import config_utils
import cmd_define

import threading
from serial_controller import *
import threading
def  mainLoop():

    # 1:get -> json ->struct ->
    serial_handler = SerialUtils()
    serial_handler.open()
    parse_handler = CmdUtils()
    thread_dict = {}
    thread_dict["data_parse"]   = 1
    thread_dict["server_post"]  = 2
    thread_dict["server_get"]   = 3
    thread_dict["serial_read"]   = threading.Thread(target=serial_handler.readLoop(),args=('') )
    thread_dict["serial_write"]  = threading.Thread(target=serial_handler.writeLoop(),args=('') )

    print thread_dict

def load_config_from_file(config_file):
    pass

if __name__  ==  "__main__" :
    parser = OptionParser()
    parser.add_option("-c", "--config", action="store_true",
                    dest="config",
                    default=None,
                    help="cmd type")
    parser.add_option("-t", "--requsetType", action="store_true",
                    dest="requsetType",
                    default='get',
                    help="http request type,just support get & post")
    parser.add_option("-s", "--server", action="store_true",
                    dest="server",
                    default='http://127.0.0.1',
                    help="http host name")
    (options, args) = parser.parse_args()

    mainLoop()


