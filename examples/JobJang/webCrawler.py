#-*- encoding: utf-8 -*-
#import requests as rs
#import bs4
from urllib.request import Request, urlopen
import urllib.parse
from bs4 import BeautifulSoup
import time
from operator import itemgetter
from datetime import datetime, date, timedelta
from jobjangDTO import Information

class Crawling:
    def getDateInNews(self, date):
        """
        기사에서 받은 날짜(YYYY-MM-DD)를 YYYYMMDD 문자열로 반환한다.
        """
        year = date[0:4]
        month = date[5:7]
        day = date[8:10]
        return year + month + day
    def getDate(self, d):
        """
        날짜 데이터를 YYYYMMDD 형식으로 뽑아준다
        """
        today = str(d.year)
        mon = ""
        if len(str(d.month)) < 2:
            mon = "0" + str(d.month)
        else:
            mon = str(d.month)
        today = today + mon
        day = ""
        if len(str(d.day)) < 2:
            day = "0" + str(d.day)
        else:
            day = str(d.day)
        today = today + day
        return today
    def getContent(self, list, w):
        """
        BS4로 추출된 기사URL에서 내용물을 뽑아낸다.
        반환형 : Information 클래스 리스트
        """
        words=[]
        for index, word in enumerate(w):
            temp = word
            words.append([temp, 0])
            #print "키워드" + word[0] + "는" + str(word[1]) + "번 나왔습니다."
        result = []
        for index, url in enumerate(list):
            #news_url = url.encode('utf-8')
            news_url = url
            #response = rs.get(news_url)
            response = Request(news_url, headers={'User-Agent':'Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)'})
            #html_content = response.text.encode(response.encoding);
            html_content = urlopen(response).read()
            #navigator = bs4.BeautifulSoup(html_content)
            navigator = BeautifulSoup(html_content , from_encoding="utf-8")

            content = navigator.find("div", id = "main_content")
            #기사 입력일 추출
            datelist = navigator.find_all("span", {"class":"t11"})
            if len(datelist) > 0 :
                datetext = datelist[0].get_text()
                datetext = self.getDateInNews(datetext)
            else :
                datetext = '20169999'
            #print datetext
            #기사 제목 추출
            header = navigator.find("h3", id = "articleTitle")
            #기사 내용 추출
            text = navigator.find(id = "articleBodyContents")
            #기사 내용과 키워드 매칭 & 카운트
            temp = "기본 0"
            c = 0
            for index, word in enumerate(words):
                #print "[%d개]"%(index) + word[0]
                word[1] = text.count("" + word[0])
                if word[1] is not 0:
                    #print "키워드(" + word[0] + ")는" + str(word[1]) + "번 나왔습니다."
                    temp = temp + " " + word[0] + " " + str(word[1])
                #print "기사에 (" + word[0] + ")이 들어가 있는 갯수 : " +str(word[1])
            #상위 5개 태그만 선별
            #temps = sorted(words, key=itemgetter(1), reverse=True)
            #내용물 SET
            info = Information()

            info.setUrl(news_url)
            info.setTitle(header)
            info.setContent(text)
            info.setPDate(datetext)
            info.setTag(temp)

            result.append(info)
            if info.getTag() != "":
                print (info.toString())
        return result

    def getUrl(self, SPAN):
        """
        네이버 뉴스 기사가 표현하는 모든 항목별, 날짜별, 페이지별 URL들을 각각 생성해 반환한다.
        """
        #sid2=731 : 모바일
        sid1s = [["IT/과학", 105]] #,["경제", 101]]
        sid2s = [["모바일", 731],["인터넷/SNS", 226], ["통신/뉴미디어", 227], \
                ["IT일반", 230], ["보안/해킹", 732], ["컴퓨터", 283], \
                ["게임/리뷰", 229], ["과학 일반", 228]]
        d = datetime.today()
        urls = []
        #SPAN은 현재날짜에서 뺀 날짜까지 긁어올 수
        for i in range(SPAN):
            date = self.getDate(d - timedelta(i))
            for sid1 in sid1s:
                for sid2 in sid2s:
                    url = "http://news.naver.com/main/list.nhn?sid2="+str(sid2[1])+"&sid1="+str(sid1[1])+"&mid=shm&mode=LS2D&date="+date
                    pages=self.getPage(url+"&page=1")
                    for page in range(pages):
                        #최종 URL(sid1, sid2, date, page별 URL)을 배열에 저장
                        final_url = url+"&page="+str(page+1)
                        urls.append(final_url)
                        #print final_url
        return urls
    def getPage(self, url):
        """
        날짜별 표현된 뉴스기사가 20개 이상인 URL은 별도의 페이지로 나누어 표현되는데,
        이를 인식하고 페이지를 카운트하여 반환한다.
        """
        #response = rs.get(url)
        response = response = Request(url, headers={'User-Agent':'Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)'})
        #html_content = response.text.encode(response.encoding)
        html_content = urlopen(response).read()
        #navigator = bs4.BeautifulSoup(html_content)
        navigator = BeautifulSoup(html_content , from_encoding="utf-8")
        pages = navigator.find("div", {"class":"paging"})
        if pages is not None:
            page_nums = pages.find_all('a')
            page_num = [item.get_text() for item in page_nums]
            return 1+len(page_num)
        return 1
    def getNews(self, SPAN):
        """
        BS4, request를 활용하여 URL별 존재하는 헤드라인 10개, 비헤드라인 10개 기사의
        주소를 리스팅한다.
        """
        url_lists = []
        naver_urls = self.getUrl(SPAN)
        len_urls = len(naver_urls)
        for i in range(len_urls):
            naver_url = naver_urls[i]
    	    #요청
            #response = rs.get(naver_url)
            response = response = Request(naver_url, headers={'User-Agent':'Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)'})
    	    #응답으로 부터 HTML 추출
            #html_content = response.text.encode(response.encoding);
            html_content = urlopen(response).read()
    	    #HTML 파싱
            #navigator = bs4.BeautifulSoup(html_content)
            navigator = BeautifulSoup(html_content , from_encoding="utf-8")
    	    #네비게이터를 이용해 원하는 링크 리스트 가져오기
            #헤드라인 10개
            headLineTags = navigator.find("ul", {"class":"type06_headline"})
            #헤드라인이 존재하는지 확인
            if headLineTags is not None:
                headLineTag = headLineTags.find_all("dt")
                resultList = [item.a for item in headLineTag]
            #비헤드라인 10개
            normalTags = navigator.find("ul", {"class":"type06"})
            #비헤드라인이 존재하는지 확인
            if normalTags is not None:
                normalTag = normalTags.find_all("dt")
                for item in normalTag:
                    resultList.append(item.a)

            #링크 추출 (중복 링크 포함)
            url_lists = url_lists + [item['href'] for item in resultList]

            #중복 링크 제거
            url_lists = list(set(url_lists))
            time.sleep(0.0001)
            #print ''
        #URL 출력
        for index, url_list in enumerate(url_lists):
            resultText = '[%d개] %s'%(index+1,url_list)
            print (resultText)
        return url_lists
"""
    daemon_flag = True;
    def Daemon():
        while (daemon_flag):
            w = [["게임", 0], ["신작", 0], ["FPS", 0]]
            getContent(getNews(), w);
            time.sleep(5)

    if __name__ == '__main__':
        Daemon()
"""
