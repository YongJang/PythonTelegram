
import pymysql
import sys
import feedparser
import urllib.parse
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import time


# -*- coding: utf-8 -*-




def getPost() :
    sleep_i = 0
    hrefs=[]  #href 가져오기 40 개
    firsthtml = Request('http://www.jobkorea.co.kr/Starter/Recruit/SS/engineering?psTab=40&rOrderTab=10&Page=1#JobList', headers={'User-Agent':'Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)'})
    sleep_i = sleep_i + 1
    firstpage = urlopen(firsthtml).read()
    firstsoup = BeautifulSoup(firstpage , from_encoding="utf-8")
    page_list = firstsoup.find("div" , { "class" : "lgiSec lgiPagination lgiPagination1" }).find_all('li') #page개수
    page_num = len(page_list)

    for page in range(page_num):
        time.sleep(3) #30*60 = 1800
        html = Request('http://www.jobkorea.co.kr/Starter/Recruit/SS/engineering?psTab=40&rOrderTab=10&Page=' + str(page) + '  #JobList', headers={'User-Agent':'Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)'})
        sleep_i = sleep_i + 1
        webpage = urlopen(html).read()
        soup = BeautifulSoup(webpage , from_encoding="utf-8")
        info = soup.find("div" , { "class" : "subject subjectNormal" }).find_all('a' : { "class" : "emp1" })
        for t in info :
            hrefs.append(t.get("href"))
            print(t.get("href"))
#
#        for index in range(0,len(hrefs)):
#            time.sleep(3) #30*60 = 1800
#            if sleep_i >= 10 :
#                sleep_i = 0
#                conn.commit()
#                time.sleep(2000)
#            detail_html = Request('http://www.jobkorea.co.kr/' + str(hrefs[index]), headers={'User-Agent':'Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)'})
#            sleep_i = sleep_i + 1
#            detailpage = urlopen(detail_html).read()
#            detailsoup = BeautifulSoup(detailpage , from_encoding="utf-8")
#            titles = detailsoup.find("span",{"class" : "title"})
#            if titles is not None :
#                print (titles.text)
#
#            date = detailsoup.find_all("dl", class_="day")
#            keyword = detailsoup.find('dt', text = '키워드').next_element.next_element.next_element.find_all("a", href = True , target ="_top")
#
#            if keyword is not None :
#                for k in range(len(keyword)) :
#                    print(k.getText())
#
#
#            for d in date:
#                datetext = d.getText().strip()
#                deadline = datetext.replace('\n', ' ')
#                #시작일 : 2016.05.05(목) 마감일 : 2016.05.11(수)
#                year = deadline[26:30]
#                month = deadline[31:33]
#                day = deadline[34:36]
#                pDate = year + month + day
#                print(pDate)
#
#                if cur.execute("""SELECT url from job where url = %s""", 'http://www.jobkorea.co.kr/' + str(hrefs[index])) < 1:
#                    cur.execute("INSERT INTO job (url, tag, content, click_num, aType, k_group, pDate) VALUES (\'http://www.jobkorea.co.kr/" + str(hrefs[index])  +"\',\'" + "소프트웨어" + "\',\' contents \' , 0, \'Job\', 0, \'" + pDate + "\');")
#                else:
#                    continue
#
#
#                    conn.commit()


def Medium_Technology():
    getPost()

if __name__ == '__main__' :
    try:
            print(sys.stdin.encoding)
            conn = pymysql.connect(host='telegramdb.cctjzlx6kmlc.ap-northeast-1.rds.amazonaws.com', port=3306, user='yongjang', passwd='yongjang', db='telegramdb', charset='utf8')
            print("connection success!!")
            cur = conn.cursor()
            Medium_Technology()

    except pymysql.Error as e:
            print ("Error %d: %s" % (e.args[0], e.args[1]))
            sys.exit(1)

    finally:
            if conn:
                    cur.close()
                    conn.close()
