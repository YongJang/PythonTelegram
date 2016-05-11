#!/usr/bin/python
#-*- coding: utf-8 -*-

# 데이터베이스를 위한 라이브러리
import os
import sys
import flask
import pymysql
from jobjangDTO import Information
from webCrawler import Crawling
application = flask.Flask(__name__)
application.debug = True
class Information:
    def __init__(self, url="", tag="", title="", content="", click_num=0, a_type="", k_group=0, p_date=""):
        self.__url = url
        self.__tag = tag
        self.__title = title
        self.__content = content
        self.__click_num = click_num
        self.__a_type = a_type
        self.__k_group = k_group
        self.__p_date = p_date
    def getUrl(self):
        return self.__url
    def setUrl(self, url):
        self.__url = url
    def getTag(self):
        return self.__tag
    def setTag(self, tag):
        self.__tag = tag
    def getTitle(self):
        return self.__title
    def setTitle(self, title):
        self.__title = title
    def getContent(self):
        return self.__content
    def setContent(self, content):
        self.__content = content
    def getClickNum(self):
        return self.__click_num
    def setClickNum(self, click_num):
        self.__click_num = click_num
    def getAType(self):
        return self.__a_type
    def setAType(self, a_type):
        self.__a_type = a_type
    def getKGroup(self):
        return self.__k_group
    def setKGroup(self, k_group):
        self.__k_group = k_group
    def getPDate(self):
        return self.__p_date
    def setPDate(self, p_date):
        self.__p_date = p_date
    def toString(self):
        return "Infomation [url="+self.__url+", tag="+self.__tag+", title="+self.__title+\
            ", pDate="+self.__p_date+"]"
# DB 연결
def __init__(self):
    """
    DB 커넥션 생성
    """
    self.db = pymysql.connect(
        user = os.getenv('MYSQL_USERNAME', 'yongjang'),
        passwd = os.getenv('MYSQL_PASSWORD', 'yongjang'),
        db = os.getenv('MYSQL_INSTANCE_NAME', 'telegramdb'),
        host = os.getenv('MYSQL_PORT_3306_TCP_ADDR', 'telegramdb.cctjzlx6kmlc.ap-northeast-1.rds.amazonaws.com'),
        port = int(os.getenv('MYSQL_PORT_3306_TCP_PORT', '3306'))
        )

    cur = self.db.cursor()
    #UTF-8 Setting
    cur.execute("set names utf8")
    reload(sys)
    sys.setdefaultencoding('utf-8')
    #cur.execute("DROP TABLE IF EXISTS rows")
    #cur.execute("CREATE TABLE rows(row INT)")
def getTags(category):
    """
    태그 DB를 모두 받아온다.
    """
    cur = self.db.cursor()
    cur.execute("SELECT * FROM tags")
    row = cur.fetchall()
    total = len(row)
    entries = []
    if total < 1:
        print 'No entries'
    else:
        for record in range(total):
            if row[record][0] == category:
                temp = row[record][1]
                entries.append(temp)
    cur.close()
    return entries
def getInfo():
    """
    기사, 채용정보를 DB에서 모두 받아온다.
    """
    cur = self.db.cursor()
    cur.execute("SELECT * FROM information")
    row = cur.fetchall()
    total = len(row)
    entries = []
    if total < 1:
        print 'No entries'
    else:
        for record in range(total):
            entry = Information()
            entry.setUrl(row[record][1])
            entry.setTag(row[record][2])
            entry.setTitle(row[record][3])
            entry.setContent(row[record][4])
            entry.setClickNum(row[record][5])
            entry.setAType(row[record][6])
            entry.setKGroup(row[record][7])
            entry.setPDate(row[record][8])
            entries.append(entry)
    cur.close()
    return entries
def setInfo(infos, type):
    """
    기사, 채용정보를 DB에 저장한다.
    """
    cur = self.db.cursor()
    for index, info in enumerate(infos):
        if type is 1:
            cur.execute('INSERT INTO information(url, tag, title, content, click_num, a_type, k_group, p_date) ' + \
                        'VALUES (\'' + info.getUrl() +'\',\'' + info.getTag() + '\',\'' + info.getTitle() + '\',\'' + \
                        info.getContent() + '\', 0, \'Article\', 0, \'' + info.getPDate() + '\')')
            print "[%d]Data Insertion Success!!"%(index+1)
        else:
            cur.execute("INSERT INTO information(url, tag, title, content, click_num, a_type, k_group, p_date) " + \
                        "VALUES (\'" + info.getUrl +"\',\'" + info.getTag + "\',\'" + info.getTitle + "\',\'" + \
                        info.getContent + "\', 0, \'Article\', 0, \'" + info.getPDate + "\')")
    cur.close()
def populate():
    cur = self.db.cursor()
    cur.execute("INSERT INTO rows(row) VALUES(520)")
def getArticle():
    cur = self.db.cursor()
    cur.execute("SELECT * FROM article")
    row = cur.fetchall()
    return row
def __del__():
    """
    DB 커넥션 해제
    """
    if self.db:
        self.db.cursor().close()
        self.db.close()
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
        temp = word.decode('utf-8')
        words.append([temp, 0])
        #print "키워드" + word[0] + "는" + str(word[1]) + "번 나왔습니다."
    result = []
    for index, url in enumerate(list):
        news_url = url.encode('utf-8')
        response = rs.get(news_url)
        html_content = response.text.encode(response.encoding);
        navigator = bs4.BeautifulSoup(html_content, 'html.parser', from_encoding='utf-8')
        content = navigator.find("div", id = "main_content")
        #기사 입력일 추출
        datetext = navigator.find("span", {"class":"t11"}).get_text()
        datetext = self.getDateInNews(datetext)
        #print datetext
        #기사 제목 추출
        header = content.h3.get_text()
        #기사 내용 추출
        text = content.find(id = "articleBodyContents").get_text()
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
            print info.toString()
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
        time.sleep(0.0001)
        #print ''
    #URL 출력
    for index, url_list in enumerate(url_lists):
        resultText = '[%d개] %s'%(index+1,url_list.encode('utf-8'))
        print resultText
    return url_lists
def main():
    reload(sys)
    sys.setdefaultencoding('utf-8')
    storage = Storage()
    crawling = Crawling()
    #storage.populate()
    #score = storage.getArticle()
    w = storage.getTags("IT")
    words = []
    #words = ["게임"]
    for index, word in enumerate(w):
        words.append(""+word)
    result = crawling.getContent(crawling.getNews(1), words);
    for index, e in enumerate(result):
        resultText = "[%d개]" % (index+1) + e.getTag() + " " + e.getPDate()
        print resultText
    storage.setInfo(result, 1)
    entries = storage.getInfo()
    for entry in entries:
        print ' URL: ' + entry.getUrl() + '\n' +\
              ' TAG: ' + entry.getTag() + '\n' +\
              ' title: ' + entry.getTitle() + '\n'
    time.sleep(5)

if __name__ == "__main__":
    main()
