#!/usr/bin/python
#-*- encoding: utf-8 -*-
import requests as rs
import bs4
import time
# JSON을 위한 라이브러리
import json
from io import StringIO
#<meta property="og:title" content="구글 조립형 스마트폰 `아라` 실물 공개.. &quot;내년 출시 예정&quot;">
#<meta property="og:type" content="article">
#<meta property="og:url" content="http://news.naver.com/main/read.nhn?mode=LSD&amp;mid=sec&amp;oid=030&amp;aid=0002480868&amp;sid1=001">
#<meta property="og:image" content="http://imgnews.naver.net/image/origin/030/2016/05/22/2480868.jpg">
#<meta property="og:description" content="구글이 마치 레고처럼 모듈 방식으로 기능을 추가할 수 있는 조립식 스마트폰 `아라`의 개발자 버전 실물을 올해 가을에 내놓고 내년부터 판매한다는 계획을 ...">
#<meta property="og:article:author" content="전자신문 | 네이버 뉴스">
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
        return "" + year + month + day

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

    def getContent(self, list, wordlist):
        """
        BS4로 추출된 기사URL에서 내용물을 뽑아낸다.
        반환형 : Information 클래스 리스트
        words : Tag 리스트
        result : 결과값
        """
        words=[]
        result = []
        for word in wordlist:
            words.append([word, 0])

        for index, url in enumerate(list):
            if url.count("sid1=105")>0:
                high_tag = "IT"
            else:
                high_tag = "경제"
            news_url = url
            response = rs.get(news_url.encode('utf-8'))
            html_content = response.text.encode(response.encoding);
            navigator = bs4.BeautifulSoup(html_content, 'html.parser', from_encoding='utf-8')
            content = navigator.find("div", id = "main_content")
            #기사 입력일 추출
            date = navigator.find("span", {"class":"t11"})
            if date is not None:
                datetext = self.getDateInNews(date.get_text()).strip().replace("\"\r\n\t", '')
                #기사 제목 추출
                header = content.h3.get_text().strip().replace("\"\r\n\t", '')
                #기사 내용 추출
                text = content.find(id = "articleBodyContents").get_text()
                text = text.strip().replace("\"\r\n\t", '')
                #기사 내용과 키워드 매칭 & 카운트(TAG)
                tags = "["
                for word in words:
                    word[1] = text.count("" + word[0])
                    if word[1] is not 0:
                        tags += "{\""+word[0]+"\":"+str(word[1])+"},"
                tags = tags[:-1]
                tags += "]"
                #기사 표현을 위한 og meta 태그 추출
                og_title = navigator.find("meta", property="og:title")
                og_type = navigator.find("meta", property="og:type")
                og_url = navigator.find("meta", property="og:url")
                og_image = navigator.find("meta", property="og:image")
                og_description = navigator.find("meta", property="og:description")
                metas = str(og_title)+str(og_type)+str(og_url)+str(og_image)+str(og_description)
                #내용물 SET
                info = Information()
                info.setUrl(news_url.replace('&','%26'))
                info.setTitle(header)
                info.setContent(text)
                info.setPDate(datetext.encode("utf8"))
                info.setHigh(high_tag)
                info.setLow(tags)
                info.setMeta(metas.replace('&','%26'))
                result.append(info)
                print('[%d개] ' % (index+1) + info.toString() + ' Original')
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
        return urls

    def getPage(self, url):
        """
        날짜별 표현된 뉴스기사가 20개 이상인 URL은 별도의 페이지로 나누어 표현되는데,
        이를 인식하고 페이지를 카운트하여 반환한다.
        """
        response = rs.get(url)
        html_content = response.text.encode(response.encoding)
        navigator = bs4.BeautifulSoup(html_content, 'html.parser', from_encoding='utf-8')
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
        #기사들 주소를 담을 변수
        url_lists = []
        naver_urls = self.getUrl(SPAN)
        len_urls = len(naver_urls)
        for i in range(len_urls):
            naver_url = naver_urls[i]
    	    #요청
            response = rs.get(naver_url)
    	    #응답으로 부터 HTML 추출
            html_content = response.text.encode(response.encoding);
    	    #HTML 파싱
            navigator = bs4.BeautifulSoup(html_content, 'html.parser', from_encoding='utf-8')
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
            time.sleep(0.000001)
        #URL 출력
        for index, url_list in enumerate(url_lists):
            resultText = '[%d개] %s'%(index+1, url_list.encode('utf8'))
            print(resultText)
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
