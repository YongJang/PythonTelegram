# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import time

firsthtml = Request('http://www.jobkorea.co.kr/Starter/Recruit/SS/engineering?psTab=40&rOrderTab=10&Page=1#JobList', headers={'User-Agent':'Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)'})
firstpage = urlopen(firsthtml).read()
firstsoup = BeautifulSoup(firstpage)
page_num = firstsoup.find("div" , { "class" : "lgiSec lgiPagination lgiPagination1" }).find_all('li') #page개수

def getPost() :
    hrefs=[]  #href 가져오기 40 개
    for page in range(0,len(page_num)):
        time.sleep(3) #30*60 = 1800
        html = Request('http://www.jobkorea.co.kr/Starter/Recruit/SS/engineering?psTab=40&rOrderTab=10&Page=' + str(page) + '  #JobList', headers={'User-Agent':'Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)'})
        webpage = urlopen(html).read()
        soup = BeautifulSoup(webpage)
        info = soup.find_all("a" ,class_="emp1")
        for t in info :
            if t.get("href") is not None :
                hrefs.append(t.get("href"))

        for index in range(0,len(hrefs)):
            time.sleep(3) #30*60 = 1800
            detail_html = Request('http://www.jobkorea.co.kr/' + str(hrefs[index]), headers={'User-Agent':'Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)'})
            detailpage = urlopen(detail_html).read()
            detailsoup = BeautifulSoup(detailpage)
            titles = detailsoup.find("span",{"class" : "title"})
            if titles is not None :
                print (titles.text)
            date = detailsoup.find_all("dl", class_="day")
            for d in date:
                datetext = d.getText().strip()
                deadline = datetext.replace('\n', ' ')
                #시작일 : 2016.05.05(목) 마감일 : 2016.05.11(수)
                year = deadline[26:30]
                month = deadline[31:33]
                day = deadline[34:36]
                pDate = year + month + day
                print(pDate)

def Medium_Technology():
    getPost()

if __name__ == '__main__' :
    Medium_Technology()
