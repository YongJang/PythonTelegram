#-*- encoding: utf-8 -*-
import requests as rs
import bs4
import time
w = [[u"게임", 0], [u"신작", 0], [u"FPS", 0]]
def getContent(list, words):
    for index, url in enumerate(list):
        #미리 긁어온 url로부터 주소 받아옴
        news_url = url.encode('utf-8')

        #요청
        response = rs.get(news_url)

        #응답으로부터 HTML 추출
        html_content = response.text.encode(response.encoding);

        #HTML 파싱
        navigator = bs4.BeautifulSoup(html_content, 'html.parser')

        #네비게이터를 이용해 원하는 링크 리스트 가져오기
        content = navigator.find("div", id = "main_content")
        #기사 입력일 추출
        datetext = navigator.find("span", {"class":"t11"}).get_text()
        print datetext
        #기사 제목 추출
        header = content.h3.get_text()
        print header
        #기사 내용 추출
        text = content.find(id = "articleBodyContents").get_text()
        #기사 내용과 키워드 매칭
        for word in words:
            print u"기사에 ("+word[0]+u")이 들어가 있는 갯수"+str(text.count(word[0]))
def getUrl():
    #sid2=731 : 모바일
    sid1s = [[u"IT/과학", 105]] #,[u"경제", 101]]
    sid2s = [[u"모바일", 731],[u"인터넷/SNS", 226], [u"통신/뉴미디어", 227], \
            [u"IT일반", 230], [u"보안/해킹", 732], [u"컴퓨터", 283], \
            [u"게임/리뷰", 229], [u"과학 일반", 228]]
    t = time.localtime()
    date = str(t.tm_year)
    mon = u""
    if len(str(t.tm_mon)) < 2 :
        mon = u"0" + str(t.tm_mon)
    else:
        mon = str(t.tm_mon)
    date = date + mon
    day = u""
    if len(str(t.tm_mday)) < 2 :
        day = u"0" + str(t.tm_mday)
    else:
        day = str(t.tm_mday)
    date = date + day

    urls = []
    for sid1 in sid1s:
        for sid2 in sid2s:
            url = u"http://news.naver.com/main/list.nhn?sid2="+str(sid2[1])+"&sid1="+str(sid1[1])+"&mid=shm&mode=LS2D&date="+date+"&page=1"
            urls.append(url)
            print url

def getTopRank():

    naver_url = 'http://news.naver.com/main/list.nhn?sid2=229&sid1=105&mid=shm&mode=LS2D&date=20160507&page=1'
	#요청
    response = rs.get(naver_url)
    #http://news.naver.com/main/list.nhn?sid2=229&sid1=105&mid=shm&mode=LS2D&date=20160507&page=1
    #http://news.naver.com/main/list.nhn?sid2=229&sid1=105&mid=shm&mode=LS2D&date=20160507&page=2
	#응답으로 부터 HTML 추출
    html_content = response.text.encode(response.encoding);

	#HTML 파싱
    navigator = bs4.BeautifulSoup(html_content, 'html.parser')

	#네비게이터를 이용해 원하는 링크 리스트 가져오기
    #헤드라인 10개
    headLineTag = navigator.find("ul", {"class":"type06_headline"}).find_all("dt")
    resultList = [item.a for item in headLineTag]
    #비헤드라인 10개
    normalTag = navigator.find("ul", {"class":"type06"}).find_all("dt")
    for item in normalTag:resultList.append(item.a)

    #링크 추출 (중복 링크 포함)
    keywords = [item['href'] for item in resultList]

    #중복 링크 제거
    keywords = list(set(keywords))

    print '============='
    print time.ctime()
    print ''

	#키워드 출력
    for index, keyword in enumerate(keywords):
        resultText = '[%d개] %s'%(index+1,keyword.encode('utf-8'))
        print resultText

    print ''
    return keywords

daemon_flag = True;
def Daemon():
    while (daemon_flag):
        getUrl();
        #getContent(getTopRank(), w);
        time.sleep(5)

if __name__ == '__main__':
    Daemon()
