# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

firsthtml = Request('http://www.jobkorea.co.kr/Starter/Recruit/SS/engineering?psTab=40&rOrderTab=10&Page=1#JobList', headers={'User-Agent':'Mozilla/5.0'})
firstpage = urlopen(firsthtml).read()
firstsoup = BeautifulSoup(firstpage)
page_num = firstsoup.find("div" , { "class" : "lgiSec lgiPagination lgiPagination1" }).find_all('li')

def getPost() :
    for page in range(len(page_num)) :
        html = Request('http://www.jobkorea.co.kr/Starter/Recruit/SS/engineering?psTab=40&rOrderTab=10&Page=' + str(page) + '  #JobList', headers={'User-Agent':'Mozilla/5.0'})
        webpage = urlopen(html).read()
        soup = BeautifulSoup(webpage)
        info_title = soup.find_all("a" ,class_="emp1") #80
        tag = ["프로그래머", "개발", "H/W", "소프트웨어", "S/W", "웹", "Web", "네트워크", "솔루션","머신", "C++", "C", "JAVA"] # 소프트웨어 = S/W # web =웹
        tag_href = []
        for i in info_title :
            for j in range(len(tag)) :
                if i.get("title") is not None and tag[j] in i.get("title") :
                    tag_href.append(i.get("href"))
                    tag_href = list(set(tag_href))


        print(tag_href)

        for index in range(len(tag_href)) :
            detail_html = Request('http://www.jobkorea.co.kr/' + str(tag_href[index]), headers={'User-Agent':'Mozilla/5.0'})
            detailpage = urlopen(detail_html).read()
            detailsoup = BeautifulSoup(detailpage)
            summary = detailsoup.find_all("div", class_="gibReadSum")
            print(summary)

            date = detailsoup.find_all("dl", class_="day")
            #date = detailsoup.find("dl",{ "class" : "day"}).find_all(text = True)
            for d in date :
                print(d.getText())

def Medium_Technology() :
    getPost()

if __name__ == '__main__' :
    Medium_Technology()
