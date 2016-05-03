import pymysql
import sys
import feedparser
import urllib.parse

try:
        print(sys.stdin.encoding)

        conn = pymysql.connect(host='telegramdb.cctjzlx6kmlc.ap-northeast-1.rds.amazonaws.com', port=3306, user='yongjang', passwd='yongjang', db='telegramdb', charset='utf8')

        print("connection success!!")

        cur = conn.cursor()



        keyword = ["인공지능","빅데이터","영화","경제"]

        for n in range(0,len(keyword)):
            url = 'http://newssearch.naver.com/search.naver?where=rss&query=' + urllib.parse.quote(keyword[n].encode("utf-8")) + '&field=0'
            d = feedparser.parse(url)
            cur.execute(pymysql.escape_string("INSERT INTO article (url, tag, content, click_num, aType, k_group, pDate) VALUES ('http://www.asiatoday.co.kr/view.php?key=20160503002218366','인공지능','이세돌 9단은 지난달 인공지능 \'알파고\'와 대결한 이후 6전 전승 무패 행진도 이어갔다. 이날 승리로 이세돌 9단은 원성진 9단에게 상대 전적 14승 11패로 더욱 앞서나갔다. 원성진 9단은 2국과 오는 18일 3국을 모두...',0,'IT',0,'20160503');"))

            for post in d.entries:
                pSummary = post.summary.replace("\'","\\'")
                cur.execute("INSERT INTO article (url, tag, content, click_num, aType, k_group, pDate) VALUES (\'" + post.link +"\',\'" + keyword[n] + "\',\'" + pSummary + "\', 0, \'IT\', 0, \'20160503\');")
                print(post.link)
                print(keyword[n])
                print(pSummary)
                print("\'20160503\'")



except pymysql.Error as e:
        print ("Error %d: %s" % (e.args[0], e.args[1]))
        sys.exit(1)

finally:
        if conn:
                cur.close()
                conn.close()
