#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
__author__ = 'Bright Jiang'

from cmd_define import *
from serial_controller import *
import threading

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
