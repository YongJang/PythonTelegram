#-*- encoding: utf-8 -*-
import requests as rs
import bs4
import time
from datetime import datetime, date, timedelta
from jobjangDTO import Information
class Crawling:
    def getDateInNews(self, date):
        u"""
        기사에서 받은 날짜(YYYY-MM-DD)를 YYYYMMDD 문자열로 반환한다.
        """
        d = u""
        d += date[0:4]
        d += date[5:7]
        d += date[8:10]
        return d
    def getDate(self, d):
        u"""
        날짜 데이터를 YYYYMMDD 형식으로 뽑아준다
        """
        today = str(d.year)
        mon = u""
        if len(str(d.month)) < 2:
            mon = u"0" + str(d.month)
        else:
            mon = str(d.month)
        today = today + mon
        day = u""
        if len(str(d.day)) < 2:
            day = u"0" + str(d.day)
        else:
            day = str(d.day)
        today = today + day
        return today
    def getContent(self, list, words):
        u"""
        BS4로 추출된 기사URL에서 내용물을 뽑아낸다.
        반환형 : Information 클래스 리스트
        """
        result = []
        for index, url in enumerate(list):
            news_url = url.encode('utf-8')
            response = rs.get(news_url)
            html_content = response.text.encode(response.encoding);
            navigator = bs4.BeautifulSoup(html_content, 'html.parser')
            content = navigator.find("div", id = "main_content")
            #기사 입력일 추출
            datetext = navigator.find("span", {"class":"t11"}).get_text()
            #print datetext
            #기사 제목 추출
            header = content.h3.get_text()
            #기사 내용 추출
            text = content.find(id = "articleBodyContents").get_text()
            #기사 내용과 키워드 매칭 & 카운트
            #print u"기사에 ("+word[0]+u")이 들어가 있는 갯수"+str(text.count(word[0]))
            for word in words:
                word[1] = text.count(word[0])
            #상위 5개 태그만 선별
            temps = sorted(words, key=lambda word:word[1], reverse=True)
            temp = u""
            for t in temps:
                temp += t[0]+u" "+str(t[1])+u" "

            #내용물 SET
            result.append(Information())
            result[index].setUrl(news_url)
            result[index].setTitle(header)
            result[index].setContent(text)
            result[index].setPDate(self.getDateInNews(datetext))
            result[index].setTag(temp)
            #print result[index].toString()
        return result

    def getUrl(self, SPAN):
        u"""
        네이버 뉴스 기사가 표현하는 모든 항목별, 날짜별, 페이지별 URL들을 각각 생성해 반환한다.
        """
        #sid2=731 : 모바일
        sid1s = [[u"IT/과학", 105]] #,[u"경제", 101]]
        sid2s = [[u"모바일", 731],[u"인터넷/SNS", 226], [u"통신/뉴미디어", 227], \
                [u"IT일반", 230], [u"보안/해킹", 732], [u"컴퓨터", 283], \
                [u"게임/리뷰", 229], [u"과학 일반", 228]]
        d = datetime.today()
        urls = []
        #SPAN은 현재날짜에서 뺀 날짜까지 긁어올 수
        for i in range(SPAN):
            date = self.getDate(d - timedelta(i))
            for sid1 in sid1s:
                for sid2 in sid2s:
                    url = u"http://news.naver.com/main/list.nhn?sid2="+str(sid2[1])+"&sid1="+str(sid1[1])+"&mid=shm&mode=LS2D&date="+date+"&page=1"
                    pages=self.getPage(url+u"&page=1")
                    for page in range(pages):
                        #최종 URL(sid1, sid2, date, page별 URL)을 배열에 저장
                        final_url = url+u"&page="+str(page+1)
                        urls.append(final_url)
                        #print final_url
        return urls
    def getPage(self, url):
        u"""
        날짜별 표현된 뉴스기사가 20개 이상인 URL은 별도의 페이지로 나누어 표현되는데,
        이를 인식하고 페이지를 카운트하여 반환한다.
        """
        response = rs.get(url)
        html_content = response.text.encode(response.encoding)
        navigator = bs4.BeautifulSoup(html_content, 'html.parser')
        pages = navigator.find("div", {"class":"paging"})
        if pages is not None:
            page_nums = pages.find_all('a')
            page_num = [item.get_text() for item in page_nums]
            return 1+len(page_num)
        return 1
    def getNews(self, SPAN):
        u"""
        BS4, request를 활용하여 URL별 존재하는 헤드라인 10개, 비헤드라인 10개 기사의
        주소를 리스팅한다.
        """
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
            navigator = bs4.BeautifulSoup(html_content, 'html.parser')
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

    	    #URL 출력
            #for index, url_list in enumerate(url_lists):
            #    resultText = '[%d개] %s'%(index+1,url_list.encode('utf-8'))
                #print resultText
            time.sleep(0.03)
            #print ''
        return url_lists
u"""
    daemon_flag = True;
    def Daemon():
        while (daemon_flag):
            w = [[u"게임", 0], [u"신작", 0], [u"FPS", 0]]
            getContent(getNews(), w);
            time.sleep(5)

    if __name__ == '__main__':
        Daemon()
"""
