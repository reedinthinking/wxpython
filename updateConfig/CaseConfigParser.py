#!/usr/bin/env python
#encoding:utf-8
import ConfigParser
class CaseConfigParser(ConfigParser.ConfigParser):
    def __init__(self,defaults=None):
        ConfigParser.ConfigParser.__init__(self,defaults=None)
    def optionxform(self, optionstr):
        return optionstr