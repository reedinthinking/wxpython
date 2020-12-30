#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import sys
#import frozenDir
#sys.path.append("..")
import ConfigParser
from updateConfig.CaseConfigParser import CaseConfigParser
class ConfigUtil(object):
    """ 处理config配置的类 """
    def __init__(self, file='config/paramConfig.ini'):
        """
        :param path:
        """
        self.file = file
        self.cf = self.load_init(self.file)
        self.cf.optionxform = str

    def load_init(self, file):
        """
        :return: 加载conf
        """
        cf = CaseConfigParser()#ConfigParser.ConfigParser()
        cf.read(file)
        return cf

    # def getAbsolutePath(self):
    #     setup_dir = frozenDir.app_path()
    #     #print "configOpt:"+setup_dir

    def get_sections(self):
        """
        :return: 获取文件所有的sections
        """
        sections = self.cf.sections()
        return sections

    def get_options(self, section):
        """
        :param section: 获取某个section所对应的键
        :return:
        """
        options = self.cf.options(section)
        return options

    def get_items(self, sections):
        """
        :param sections: 获取某个section所对应的键值对
        :return:
        """
        items = self.cf.items(sections)
        return items

    def get_value(self, section, key):
        """
        :param sections:
        :param key:
        :return: 获取某个section某个key所对应的value
        """
        value = self.cf.get(section, key)
        return value

    # get_int获取整型，section区域名, option选项名
    def get_int(self, section, option):
        return self.cf.getint(section, option)

    # get_float获取浮点数类型，section区域名, option选项名
    def get_float(self, section, option):
        return self.cf.getfloat(section, option)

    # get_boolean获取布尔类型，section区域名, option选项名
    def get_boolean(self, section, option):
        return self.cf.getboolean(section, option)

    # get_eval_data获取列表，section区域名, option选项名
    def get_eval_data(self, section, option):
        return eval(self.cf.get(section, option))

    def has_section(self,section_name):
        return self.cf.has_section(section_name)

    def has_option(self,section_name,option_name):
        return self.cf.has_option(section_name,option_name)

    def remove_section(self, section):
        """
        删除section
        :param section:
        :param key:
        :return:
        """
        self.cf.remove_section(section)

    def remove_option(self, section, key):
        """
        删除option
        :param section:
        :param key:
        :return:
        """
        self.cf.remove_option(section, key)

    def add_section(self, section):
        """
        添加section
        :param section:
        :return:
        """
        self.cf.add_section(section)

    def set_item(self, section, key, value):
        """
        给指定的Section设置key,value
        :param section:
        :param key:
        :param value:
        :return:
        """
        self.cf.set(section, key, value)

    def save(self):
        """
        保存配置文件
        :return:
        """
        fp = open(self.configFilePath, 'w')  # with open(self.configFilePath,"w+") as f:self.cf.write(f)
        self.cf.write(fp)
        fp.close()

    def write_config(self,datas):
        """
        写入配置操作
        :param datas: 需要传入写入的数据
        :param filename: 指定文件名
        :return:
        """
        # 做校验，为嵌套字典的字典或字典的列表才可以
        if isinstance(datas, dict):  # 遍历，在外层判断是否为字典
            # 再来判断内层的 values 是否为字典
            for value in datas.values():  # 先取出value
                if not isinstance(value, dict):  # 在判断
                    print "数据不合法, 应为嵌套字典的字典"

            for key in datas:  # 写入操作
                #print key
                #print datas[key]
                # if not self.has_section(key):
                #     self.add_section(key)
                # self.cf[key] = datas[key]
                for key in datas:  # 写入操作
                    #print "+++++++++++++++++++++++++++++++++++++"
                    #print type(datas[key])
                    if not self.has_section(key):
                        self.add_section(key)
                    for key2 in datas[key]:
                        self.set_item(key, key2, datas[key][key2])
            with open(self.file, "w+") as file:  # 保存到哪个文件filename=需要指定文件名
                self.cf.write(file)
                file.close()
            #print "xieru chenggong"
                # return "写入成功"

    def update_config(self,datas):
        """
        写入配置操作
        :param datas: 需要传入写入的数据
        :param filename: 指定文件名
        :return:
        """
        # 做校验，为嵌套字典的字典才可以
        if isinstance(datas, dict):  # 遍历，在外层判断是否为字典
            # 再来判断内层的 values 是否为字典
            for value in datas.values():  # 先取出value
                if not isinstance(value, dict):  # 在判断
                    print "数据不合法, 应为嵌套字典的字典"

            for key in datas:  # 写入操作
                if not self.has_section(key):
                    self.add_section(key)
                for key2 in datas[key]:
                    self.set_item(key,key2,datas[key][key2])
            with open(self.file, "w+") as file:  # 保存到哪个文件filename=需要指定文件名
                self.cf.write(file)
                file.close()
            #print "写入成功"

    def saveConfig(self):
        with open(self.file, "w+") as file:  # 保存到哪个文件filename=需要指定文件名
            self.cf.write(file)
            file.close()
if __name__ == "__main__":
    """ 测试函数 """
    pwd = os.getcwd()
    file = os.path.abspath(os.path.dirname(pwd) + os.path.sep + ".") + '/paramConfig.ini'
    print file
    myconfig = ConfigUtil(file)
    print myconfig.get_sections()
    print myconfig.get_options('1297775230043774978')
    print myconfig.get_value('1297775230043774978', 'operationtimespan')
    # dict2 = {'1297775230043774978':{'abnormalstarttime':'66666'},'123456':{'abnormalstarttime':'66666'}}
    # print isinstance(dict2, dict)
    # myconfig.write_config(dict2)
    paramsinfo = myconfig.get_items('1297775230043774978')
