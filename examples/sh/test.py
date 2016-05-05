# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import time

firsthtml = Request('http://www.jobkorea.co.kr/Starter/Recruit/SS/engineering?psTab=40&rOrderTab=10&Page=1#JobList', headers={'User-Agent':'Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)'})
firstpage = urlopen(firsthtml).read()
firstsoup = BeautifulSoup(firstpage)
page_num = firstsoup.find("div" , { "class" : "lgiSec lgiPagination lgiPagination1" }).find_all('li') #page개수

def getPost() :
    i = 17001522
    hrefs=[]  #href 가져오기 40 개
    for page in range(1,100):
        time.sleep(1)
        html = Request('http://www.jobkorea.co.kr/Recruit/GI_Read/' + str(i) + '?Oem_Code=C1&rPageCode=ST&PageGbn=ST', headers={'User-Agent':'Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)'})
        webpage = urlopen(html).read()
        soup = BeautifulSoup(webpage)
        info = soup.find_all("span" ,class_="title")
        print (i)
        i = i+1
        print (info.text)
    print("!!!!!")



def Medium_Technology():
    getPost()

if __name__ == '__main__' :
    Medium_Technology()
