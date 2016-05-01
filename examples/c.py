#-*- encoding: utf-8 -*-
import requests as rs
import bs4
import time

def getArticle() :
    medium_technology_url = 'https://medium.com/browse/b99480981476'

    response = rs.get(medium_technology_url)

    html_content = response.text.encode(response.encoding);

    navigator = bs4.BeautifulSoup(html_content)

    articleHeader = navigator.find_all('h3')

    print articleHeader.decode('utf-8').encode('utf-8')

def Medium_Technology() :
    getArticle()

if __name__ == '__main__' :
    Medium_Technology()
