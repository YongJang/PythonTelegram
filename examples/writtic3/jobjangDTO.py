#!/usr/bin/python
#-*- coding: utf-8 -*-
class Information:
    def __init__(self, url=u"", tag=u"", title=u"", content=u"", click_num=0, a_type=u"", k_group=0, p_date=u""):
        self.__url = url
        self.__tag = tag
        self.__title = title
        self.__content = content
        self.__click_num = click_num
        self.__a_type = a_type
        self.__k_group = k_group
        self.__p_date = p_date
    def getUrl(self):
        return self.__url
    def setUrl(self, url):
        self.__url = url
    def getTag(self):
        return self.__tag
    def setTag(self, tag):
        self.__tag = tag
    def getTitle(self):
        return self.__title
    def setTitle(self, title):
        self.__title = title
    def getContent(self):
        return self.__content
    def setContent(self, content):
        self.__content = content
    def getClickNum(self):
        return self.__click_num
    def setClickNum(self, click_num):
        self.__click_num = click_num
    def getAType(self):
        return self.__a_type
    def setAType(self, a_type):
        self.__a_type = a_type
    def getKGroup(self):
        return self.__k_group
    def setKGroup(self, k_group):
        self.__k_group = k_group
    def getPDate(self):
        return self.__p_date
    def setPDate(self, p_date):
        self.__p_date = p_date
    def toString(self):
        return 'Infomation [url='+self.__url+', tag='+self.__tag+', title='+self.__title+\
            ', pDate='+self.__p_date+']'
