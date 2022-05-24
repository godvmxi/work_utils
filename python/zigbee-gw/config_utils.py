#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
__author__ = 'Bright Jiang'
import ConfigParser
import string, os, sys

class ConfigUtils():
    def __init__(self,cfg):
        self.configFile = cfg
        if not os.path.isfile(self.configFile) :
            raise Exception('config file is not exist')
        self.handler =  ConfigParser.ConfigParser()
        self.handler.read(self.configFile)
        self.sectionList = self.handler.sections()
    def getSectionList(self):
        return self.sectionList
    def getSectionKey(self,sec,key):
        if sec in self.sectionList:
            return self.handler.get(sec,key)
        else :
            raise Exception("target section is not exist")
        pass
    def getAll(self):
        pass
    def setSectionKey(self,key,value):
        '''
        Args:
            dic:
            will add soon if needed
        Returns:

        '''
    def getAll(self):
        result = {}
        for sec in self.sectionList :
            temp = {}
            for item in self.handler.items(sec):
                temp[item[0]] = item[1]
            result[sec] =  temp
        return result
        pass
if __name__  ==  "__main__" :
    cf = ConfigUtils("config.ini")
    print cf.getSectionList()
    print cf.getSectionKey('server','hostname')
    print cf.getSectionKey('server','port')
    print cf.getAll()