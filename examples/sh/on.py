# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

def getPost() :

    html = Request('http://www.jobkorea.co.kr/net/Starter/Recruit/SS/engineering?rOrderTab=10#JobList', headers={'User-Agent':'Mozilla/5.0'})
    webpage = urlopen(html).read()
    soup = BeautifulSoup(webpage)

    info_title = soup.find_all("a" ,class_="emp1")
    tag = ["소프트웨어", "프로그래머"]

    page_num = soup.find_all("div" ,class_="lgiSec lgiPagination lgiPagination1")
    page_ul = page_num.parent.find_next_sibling()

    for item in page_ul.find_all('li'):
        if isinstance(item, tag):
            print item.text
    #print (len(page_num))
    '''
    for page in range(1,page_num):
   	    html = Request('http://www.jobkorea.co.kr/Starter/Recruit/SS/engineering?psTab=40&rOrderTab=10&Page=' + page + '  #JobList', headers={'User-Agent':'Mozilla/5.0'})
            for i in info_title:
                for j in range(len(tag)) :
                    if i.get("title") is not None and tag[j] in i.get("title"):
                        print (i.get("title"))
                    else:
                        print ("nothing")
'''
def Medium_Technology() :
    getPost()

if __name__ == '__main__' :
    Medium_Technology()
