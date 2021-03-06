
import pymysql
import sys
import feedparser
import urllib.parse
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import time

try:
        print(sys.stdin.encoding)
        conn = pymysql.connect(host='telegramdb.cjks7yer9qjg.ap-northeast-2.rds.amazonaws.com', port=3306, user='yongjang', passwd='yongjang', db='telegramdb', charset='utf8')
        print("connection success!!")
        cur = conn.cursor()
# -*- coding: utf-8 -*-

        firsthtml = Request('http://www.jobkorea.co.kr/Starter/Recruit/SS/engineering?psTab=40&rOrderTab=10&Page=1#JobList', headers={'User-Agent':'Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)'})
        firstpage = urlopen(firsthtml).read()
        firstsoup = BeautifulSoup(firstpage , from_encoding="utf-8")
        page_num = firstsoup.find("div" , { "class" : "lgiSec lgiPagination lgiPagination1" }).find_all('li') #page개수

        def getPost() :
            for page in range(1,4):
                time.sleep(1)
                html = Request('http://www.jobkorea.co.kr/Recruit/GI_Read/17067787?Oem_Code=C1&rPageCode=ST&PageGbn=ST', headers={'User-Agent':'Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)'})
                webpage = urlopen(html).read()
                soup = BeautifulSoup(webpage, from_encoding="utf-8")
                info = soup.find_all(class_="title")

                calendar = soup.find_all("dl", class_="day") # 상세페이지의 마감일 찾기 (달력 형식)
                date_second = soup.find_all("p", class_="regular") # 다른 형식의 상세페이지의 마감일 (달력없는 형식)
                keywords = soup.find("dt", text = "키워드").next_element.next_element.next_element.find_all("a", href = True , target ="_top")
                for k in keywords :
                    print(k.getText())

                pDate = ""
                print("testtt")
                if calendar :
                    for d in calendar:
                        datetext = d.getText().strip()
                        deadline = datetext.replace('\n', ' ')
                        year = deadline[26:30]
                        month = deadline[31:33]
                        day = deadline[34:36]
                        pDate = year + month + day
                        print("calendar에 들어왔습니다.")
                        print(pDate)

                elif date_second :
                    for d in date_second:
                        datetext = d.getText().strip()
                        deadline = datetext.replace('.', ' ')
                        year = deadline[17:21]
                        month = deadline[22:24]
                        day = deadline[25:27]
                        pDate = year + month + day
                        print("date_second에 들어왔습니다.")
                        print(pDate)
                else :
                    print("else 문 에 들어왔습니다.")
                print(pDate)

                cur.execute("INSERT INTO testjob (url, tag, content, click_num, aType, k_group, pDate) VALUES (\'http://www.jobkorea.co.kr/Recruit/GI_Read/17067787?Oem_Code=C1&rPageCode=ST&PageGbn=ST\',\'" + "소프트웨어" + "\',\' contents \' , 0, \'Job\', 0, \'" + pDate + "\');")

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
