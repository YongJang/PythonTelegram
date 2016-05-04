import pymysql
import sys
import feedparser
import urllib.parse

try:
        print(sys.stdin.encoding)

        conn = pymysql.connect(host='telegramdb.cctjzlx6kmlc.ap-northeast-1.rds.amazonaws.com', port=3306, user='yongjang', passwd='yongjang', db='telegramdb', charset='utf8')

        print("connection success!!")

        cur = conn.cursor()



        keyword = ["웹","빅데이터"]

        for index in range(len(tag_href)):
            url = 'http://www.jobkorea.co.kr/' + str(tag_href[index])+ urllib.parse.quote(keyword[index].encode("utf-8")) + '&field=0'
            d = feedparser.parse(url)

            for post in d.entries:
                #pSummary = post.summary.replace("\'","\\\'")
                cur.execute("INSERT INTO job (url, tag, content, click_num, aType, k_group, pDate) VALUES (\'" + post.link +"\',\'" + keyword[index] + "\',\'" + '' + "\', 0, \'IT\', 0, \'20160503\');")
                print (post.published)

        conn.commit()

except pymysql.Error as e:
        print ("Error %d: %s" % (e.args[0], e.args[1]))
        sys.exit(1)

finally:
        if conn:
                cur.close()
                conn.close()
