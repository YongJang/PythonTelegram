
import pymysql
import sys
import feedparser
from urllib.request import Request, urlopen
import urllib.parse
from bs4 import BeautifulSoup
import time
import json
import collections

try:
        print(sys.stdin.encoding)
        conn = pymysql.connect(host='telegramdb.cctjzlx6kmlc.ap-northeast-1.rds.amazonaws.com', port=3306, user='yongjang', passwd='yongjang', db='telegramdb', charset='utf8')
        print("connection success!!")
        cur = conn.cursor()
# -*- coding: utf-8 -*-

        sleep_i = 0
        firsthtml = Request('http://www.jobkorea.co.kr/Starter/Recruit/SS/engineering?psTab=40&rOrderTab=10&Page=1#JobList', headers={'User-Agent':'Mozilla/15.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)'})
        sleep_i = sleep_i + 1
        firstpage = urlopen(firsthtml).read()
        firstsoup = BeautifulSoup(firstpage , from_encoding="utf-8")
        page_num = firstsoup.find("div" , { "class" : "lgiSec lgiPagination lgiPagination1" }).find_all('li') #page개수
        #href 가져오기 40 개
        def getPost(sleep_i) :
            hrefs=[]  #href 가져오기 40 개
            k_list = []
            tag_str = ""
            for page in range(0,len(page_num)):
                time.sleep(3) #30*60 = 1800
                html = Request('http://www.jobkorea.co.kr/Starter/Recruit/SS/engineering?psTab=40&rOrderTab=10&Page=' + str(page) + '  #JobList', headers={'User-Agent':'Mozilla/15.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)'})
                sleep_i = sleep_i + 1
                webpage = urlopen(html).read()
                soup = BeautifulSoup(webpage , from_encoding="utf-8")
                info = soup.find_all("a" ,onclick="GI_Click_Cnt('ST','B02');") # href 찾기
                for t in info :
                    if t.get("href") is not None :
                        hrefs.append(t.get("href"))

                for index in range(0,len(hrefs)): # 40
                    db_tags = []
                    json_tags = []
                    tag_str = ""
                    time.sleep(2)
                    i_ip = 1
                    if sleep_i >= 23 :
                        i_ip = i_ip + 1
                        #detail_html = Request('http://www.jobkorea.co.kr/' + str(hrefs[index]), headers={'User-Agent':'Mozilla/'+str(i_ip)+'.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)'})
                        #sleep_i = 0
                        #conn.commit()
                        #time.sleep(1803)
                        detail_html = Request('http://www.jobkorea.co.kr/' + str(hrefs[index]), headers={'User-Agent':'Mozilla/'+str(i_ip)+'.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)'})
                        sleep_i = sleep_i + 1 # 상세페이지 들어가기
                        detailpage = urlopen(detail_html).read()
                        detailsoup = BeautifulSoup(detailpage , from_encoding="utf-8")
                        titles = detailsoup.find("span",{"class" : "title"})
                        if titles is not None : # 상세페이지의 title
                            db_title = titles.text.strip()

                        calendar = detailsoup.find_all("dl", class_="day") # 상세페이지의 마감일 찾기 (달력 형식)
                        date_second = detailsoup.find_all("p", class_="regular") # 다른 형식의 상세페이지의 마감일 (달력없는 형식)
                        keyword = detailsoup.find('dt', text = '키워드').next_element.next_element.next_element.find_all("a", href = True , target ="_top") # 상세페이지의 키워드 찾기

                        if keyword is not None :
                            weight = "15" # 가중치
                            for k in keyword :
                                k_list.append(k.text) # k_list에 키워드text 넣기

                            for k_count in range(len(k_list)) :
                                if cur.execute("""SELECT * from tags where low = %s""", str(k_list[k_count])) > 0 :
                                    db_tags.append(k_list[k_count]) # low == tags

                            for n in range(len(db_tags)) :
                                db_tags[n] = json.dumps(db_tags[n] , ensure_ascii=False, sort_keys=False)
                                tag_str = tag_str + "{" + str(db_tags[n]) + ":" + weight + "},"
                            tag_str = tag_str[:-1]
                            print(len(tag_str))
                            db_tags.clear()
                            k_list.clear()
                        print(tag_str)

                        pDate = ""
                        if calendar  :
                            for d in calendar:
                                datetext = d.getText().strip()
                                deadline = datetext.replace('\n', ' ')
                                year = deadline[26:30]
                                month = deadline[31:33]
                                day = deadline[34:36]
                                pDate = year + month + day
                                print(pDate)

                        elif date_second :
                            for d in date_second:
                                datetext = d.getText().strip()
                                deadline = datetext.replace('.', ' ')
                                year = deadline[17:21]
                                month = deadline[22:24]
                                day = deadline[25:27]
                                pDate = year + month + day
                                print(pDate)
                        else :
                            break

                        if cur.execute("""SELECT url from jobs where url = %s""", 'http://www.jobkorea.co.kr/' + str(hrefs[index])) < 1 and  len(tag_str) > 4:
                            cur.execute("INSERT INTO jobs (url, high , low , title, content, click_num, aType, k_group, pDate) VALUES (\'http://www.jobkorea.co.kr/" + str(hrefs[index])  +"\',\' IT \',\'[" + str(tag_str) + "]\',\'"+ str(db_title) + "\' ,\' contents \' , 0, \'Job\', 0, \'" + pDate + "\');")
                            conn.commit()
                        else :
                            continue

        def Medium_Technology():
            getPost(sleep_i)

        if __name__ == '__main__' :
            Medium_Technology()
except pymysql.Error as e:
    print ("Error %d: %s" % (e.args[0], e.args[1]))
    sys.exit(1)

finally:
    if conn:
            cur.close()
            conn.close()
