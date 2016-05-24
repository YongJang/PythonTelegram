#!/usr/bin/python
#-*- coding: utf-8 -*-
class Information:
    def __init__(self, url="", high="", low="", title="", content="", click_num=0, a_type="", k_group=0, p_date="", meta=""):
        self.__url = url
        self.__high = high
        self.__low = low
        self.__title = title
        self.__content = content
        self.__click_num = click_num
        self.__a_type = a_type
        self.__k_group = k_group
        self.__p_date = p_date
        self.__meta = meta
    def getUrl(self):
        return self.__url
    def setUrl(self, url):
        self.__url = url
    def getHigh(self):
        return self.__high
    def setHigh(self, high):
        self.__high = high
    def getLow(self):
        return self.__low
    def setLow(self, low):
        self.__low = low
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
    def getMeta(self):
        return self.__meta
    def setMeta(self, meta):
        self.__meta = meta
    def toString(self):
        return "Infomation [url="+str(self.__url)+", tag="+str(self.__low)+", title="+str(self.__title)+\
            ", pDate="+str(self.__p_date)+"]"
