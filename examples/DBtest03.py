import pymysql
import sys
import feedparser
import urllib.parse

try:
        print(sys.stdin.encoding)

        conn = pymysql.connect(host='telegramdb.cctjzlx6kmlc.ap-northeast-1.rds.amazonaws.com', port=3306, user='yongjang', passwd='yongjang', db='telegramdb', charset='utf8')

        print("connection success!!")

        cur = conn.cursor()



        keyword = ["인공지능"]

        for n in range(0,len(keyword)):
            url = 'http://newssearch.naver.com/search.naver?where=rss&query=' + urllib.parse.quote(keyword[n].encode("utf-8")) + '&field=0'
            d = feedparser.parse(url)

            cur.execute("""SELECT url from article""")
            urlData = cur.fetchall()

            print ("urlData : " +urlData)

            for post in d.entries:
                pSummary = post.summary.replace("\'","\\\'")
                pDate = post.published
                #Wed, 04 May 2016 11:26:00 +0900
                month = pDate[8:11]
                if month == 'Jan':
                    month = '01'
                elif month == 'Feb':
                    month = '02'
                elif month == 'Mar':
                    month = '03'
                elif month == 'Apr':
                    month = '04'
                elif month == 'May':
                    month = '05'
                elif month == 'Jun':
                    month = '06'
                elif month == 'Jul':
                    month = '07'
                elif month == 'Aug':
                    month = '08'
                elif month == 'Sep':
                    month = '09'
                elif month == 'Oct':
                    month = '10'
                elif month == 'Nov':
                    month = '11'
                else:
                    month ='12'

                day = pDate[5:7]
                year = pDate[12:16]
                pDate = year + month + day

                if post.link not in urlData:
                    cur.execute("INSERT INTO article (url, tag, content, click_num, aType, k_group, pDate) VALUES (\'" + post.link +"\',\'" + keyword[n] + "\',\'" + pSummary + "\', 0, \'Article\', 0, \'" + pDate + "\');")
                else:
                    continue


        conn.commit()

except pymysql.Error as e:
        print ("Error %d: %s" % (e.args[0], e.args[1]))
        sys.exit(1)

finally:
        if conn:
                cur.close()
                conn.close()
