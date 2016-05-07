import pymysql
import sys
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

def getPost() :
    html = Request('http://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid1=105&sid2=230', headers={'User-Agent':'Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)'})
    page = urlopen(html).read()
    soup = BeautifulSoup(page , from_encoding="utf-8")
    page_num_list = soup.find("div" , { "class" : "paging" }).find_all('a') #page개수
    page_num = len(page_num_list)
    print("page_num = page_num")


def Naver_IT_News() :
    getPost()

if __name__ == '__main__' :
    try:
            print(sys.stdin.encoding)
            conn = pymysql.connect(host='telegramdb.cctjzlx6kmlc.ap-northeast-1.rds.amazonaws.com', port=3306, user='yongjang', passwd='yongjang', db='telegramdb', charset='utf8')
            print("Database connection success!!")
            cur = conn.cursor()
            Naver_IT_News()
    except pymysql.Error as e:
            print ("Error %d: %s" % (e.args[0], e.args[1]))
            sys.exit(1)

    finally:
            if conn:
                    cur.close()
                    conn.close()
