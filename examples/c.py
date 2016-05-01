#-*- encoding: utf-8 -*-
import requests as rs
import bs4 import BeautifulSoup
import urllib2
import time

def getArticle() :
    medium_technology_url = 'https://medium.com/browse/b99480981476'

    content = urllib2.urlopen(medium_technology_url).read()

    soup = BeautifulSoup(content)

    print soup.prettify()

    print h3
    >> 'h3'? A year and a half with Alexa

    print soup.h3.string
    >> ? A year and a half with Alexa

    print soup
    print soup.a
    A year and a half with Alexa

    #response = rs.get(medium_technology_url)

    #html_content = response.text.encode(response.encoding);

    #navigator = bs4.BeautifulSoup(html_content)

    #articleHeader = navigator.find_all('h3')

    #for keyword in enumerate(articleHeader):
	#	resultText = '%s'%(keyword.encode('utf-8'))
    #    print resultText

    #print ''

def Medium_Technology() :
    getArticle()

if __name__ == '__main__' :
    Medium_Technology()
