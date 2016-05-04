import pymysql
import sys
import feedparser
import urllib.parse

try:
        print(sys.stdin.encoding)

        conn = pymysql.connect(host='telegramdb.cctjzlx6kmlc.ap-northeast-1.rds.amazonaws.com', port=3306, user='yongjang', passwd='yongjang', db='telegramdb', charset='utf8')

        print("connection success!!")

        cur = conn.cursor()



        keyword = ["인공지능","빅데이터"]

        for n in range(0,len(keyword)):
            url = 'http://newssearch.naver.com/search.naver?where=rss&query=' + urllib.parse.quote(keyword[n].encode("utf-8")) + '&field=0'
            d = feedparser.parse(url)



            for post in d.entries:
                pSummary = post.summary.replace("\'","\\\'")
                cur.execute("INSERT INTO article (url, tag, content, click_num, aType, k_group, pDate) VALUES (\'" + post.link +"\',\'" + keyword[n] + "\',\'" + pSummary + "\', 0, \'IT\', 0, \'20160503\');")
                print(post.link)
                print(keyword[n])
                print(pSummary)
                print("\'20160503\'")

        conn.commit()

except pymysql.Error as e:
        print ("Error %d: %s" % (e.args[0], e.args[1]))
        sys.exit(1)

finally:
        if conn:
                cur.close()
                conn.close()
