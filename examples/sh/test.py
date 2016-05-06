
import pymysql
import sys
import feedparser
import urllib.parse
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import time

try:
        print(sys.stdin.encoding)

        conn = pymysql.connect(host='telegramdb.cctjzlx6kmlc.ap-northeast-1.rds.amazonaws.com', port=3306, user='yongjang', passwd='yongjang', db='telegramdb', charset='utf8')

        print("connection success!!")

        cur = conn.cursor()
# -*- coding: utf-8 -*-

        firsthtml = Request('http://www.jobkorea.co.kr/Starter/Recruit/SS/engineering?psTab=40&rOrderTab=10&Page=1#JobList', headers={'User-Agent':'Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)'})
        firstpage = urlopen(firsthtml).read()
        firstsoup = BeautifulSoup(firstpage)
        page_num = firstsoup.find("div" , { "class" : "lgiSec lgiPagination lgiPagination1" }).find_all('li') #page개수

        def getPost() :
            i = 17001522
            hrefs=[]  #href 가져오기 40 개
            for page in range(1,3):
                time.sleep(1)
                html = Request('http://www.jobkorea.co.kr/Recruit/GI_Read/' + str(i) + '?Oem_Code=C1&rPageCode=ST&PageGbn=ST', headers={'User-Agent':'Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)'})
                webpage = urlopen(html).read()
                soup = BeautifulSoup(webpage)
                info = soup.find_all(class_="title")
                #date = soup.find("dl",{ "class" : "day"}).find_all("dd")
                date = soup.find_all("dl", class_="day")

                for d in date:
                    datetext = d.getText().strip()
                    deadline = datetext.replace('\n', ' ')
                    #시작일 : 2016.05.05(목) 마감일 : 2016.05.11(수)

                    year = deadline[26:30]
                    month = deadline[31:33]
                    day = deadline[34:36]
                    pDate = year + month + day
                    print(pDate)

                if cur.execute("""SELECT url from job where url = %s""", 'http://www.jobkorea.co.kr/' + str(i) + '?Oem_Code=C1&rPageCode=ST&PageGbn=ST') < 1:
                    cur.execute("INSERT INTO job (url, tag, content, click_num, aType, k_group, pDate) VALUES (\'http://www.jobkorea.co.kr/" + str(i) + "?Oem_Code=C1&rPageCode=ST&PageGbn=ST\',\'" + "소프트웨어" + "\',\' contents \' , 0, \'Job\', 0, \'" + pDate + "\');")
                else:
                    continue

            conn.commit()


        def Medium_Technology():
            getPost()

        if __name__ == '__main__' :
            Medium_Technology()

except pymysql.Error as e:
        print ("Error %d: %s" % (e.args[0], e.args[1]))
        sys.exit(1)

finally:
        if conn:
                cur.close()
                conn.close()
