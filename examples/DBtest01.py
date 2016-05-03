import pymysql
import sys

try:
        print(sys.stdin.encoding)

        conn = pymysql.connect(host='telegramdb.cctjzlx6kmlc.ap-northeast-1.rds.amazonaws.com', port=3306, user='yongjang', passwd='yongjang', db='telegramdb', charset='utf8')

        print("connection success!!")

        cur = conn.cursor()

        

except pymysql.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)

finally:
        if conn:
                cur.close()
                conn.close()
