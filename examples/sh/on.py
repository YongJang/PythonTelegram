# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

firsthtml = Request('http://www.jobkorea.co.kr/Starter/Recruit/SS/engineering?psTab=40&rOrderTab=10&Page=1#JobList', headers={'User-Agent':'Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)'})
firstpage = urlopen(firsthtml).read()
firstsoup = BeautifulSoup(firstpage)
page_num = firstsoup.find("div" , { "class" : "lgiSec lgiPagination lgiPagination1" }).find_all('li') #page개수

def getPost() :
    hrefs=[]
    for page in range(len(page_num)):
        html = Request('http://www.jobkorea.co.kr/Starter/Recruit/SS/engineering?psTab=40&rOrderTab=10&Page=' + str(page) + '  #JobList', headers={'User-Agent':'Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)'})
        webpage = urlopen(html).read()
        soup = BeautifulSoup(webpage)
        #title
        #soup.find_all("a" ,class_="emp1")
        info = soup.find_all("a" ,class_="emp1")  #href 가져오기 40 개
        for t in info :
            if t.get("href") is not None :
                hrefs.append(t.get("href"))

    for index in range(len(hrefs)):
        detail_html = Request('http://www.jobkorea.co.kr/' + str(hrefs[index]), headers={'User-Agent':'Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)'})
        detailpage = urlopen(detail_html).read()
        detailsoup = BeautifulSoup(detailpage)
        titles = detailsoup.find("span",{"class" : "title"})
        print (title)
        date = detailsoup.find_all("dl", class_="day")
        #date = detailsoup.find("dl",{ "class" : "day"}).find_all(text = True)
        for d in date:
            datetext = d.getText().replace('.', '')
            print(datetext)


        #tags = ["프로그래머", "개발", "소프트웨어","웹","S/W","H/W","솔루션"]

def Medium_Technology():
    getPost()

if __name__ == '__main__' :
    Medium_Technology()
