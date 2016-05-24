#!/usr/bin/python
#-*- coding: utf-8 -*-
import os
import sys
import flask
# 데이터베이스를 위한 라이브러리
import re
import pymysql
# JSON을 위한 라이브러리
import json
import collections
# Apache-Spark를 위한 라이브러리
# 크롤링을 위한 라이브러리
from jobjangDTO import Information
from webCrawler import Crawling
application = flask.Flask(__name__)
application.debug = True
@application.route('/')
def hello_world():
    storage = Storage()
    storage.populate()
    row = storage.row()
    return "Are you OK %d!" % row
class Storage():
    def __init__(self):
        self.db = pymysql.connect(
            user = os.getenv('MYSQL_USERNAME', 'yongjang'),
            passwd = os.getenv('MYSQL_PASSWORD', 'yongjang'),
            db = os.getenv('MYSQL_INSTANCE_NAME', 'telegramdb'),
            host = os.getenv('MYSQL_PORT_3306_TCP_ADDR', 'telegramdb.cctjzlx6kmlc.ap-northeast-1.rds.amazonaws.com'),
            port = int(os.getenv('MYSQL_PORT_3306_TCP_PORT', '3306')),
            charset ='utf8',
            use_unicode=False,
            init_command='SET NAMES UTF8'
            )
        cur = self.db.cursor()
        print("connection success!!")
        print(sys.stdin.encoding)
    def stripslashes(self, s):
        r = re.sub(r"\\(n|r)", "\n", s)
        r = re.sub(r"\\", "", r)
        return r
    def escape(self, s):
        '''
        따옴표, 쌍따옴표 등 SQL 쿼리문에서 문자로 처리되어야 할 것들에 ESCAPE문을 걸어준다.
        '''
        if s is None: return None
        return pymysql.escape_string(s)
    def getTags(self, category):
        '''
        태그 DB를 모두 받아온다.
        '''
        cur = self.db.cursor()
        cur.execute('SELECT * FROM tags')
        row = cur.fetchall()
        total = len(row)
        entries = []
        if total < 1:
            print('No entries')
        else:
            for record in range(total):
                if row[record][0].decode('utf8', 'surrogatepass') == category:
                    temp = row[record][1].decode('utf8', 'surrogatepass')
                    entries.append(temp)
        return entries
    def getInfo(self):
        """
        기사, 채용정보를 DB에서 모두 받아온다.
        """
        cur = self.db.cursor()
        sql = """SELECT * FROM information"""
        cur.execute(sql)
        row = cur.fetchall()
        total = len(row)
        entries = []
        if total < 1:
            print('No entries')
        else:
            for record in range(total):
                entry = Information()
                entry.setUrl(row[record][1].decode('utf8', 'surrogatepass'))
                entry.setHigh(row[record][2].decode('utf8', 'surrogatepass'))
                entry.setLow(row[record][3].decode('utf8', 'surrogatepass'))
                entry.setTitle(row[record][4].decode('utf8', 'surrogatepass'))
                entry.setContent(row[record][5].decode('utf8', 'surrogatepass'))
                entry.setClickNum(row[record][6])
                entry.setAType(row[record][7].decode('utf8', 'surrogatepass'))
                entry.setKGroup(row[record][8])
                entry.setPDate(row[record][9].decode('utf8', 'surrogatepass'))
                entry.setMeta(row[record][10].decode('utf8', 'surrogatepass'))
                entries.append(entry)
        return entries

    def setInfo(self, infos, t):
        '''
        기사, 채용정보를 DB에 저장한다.
        TAG는 JSON 타입으로 저장한다.
        '''
        cur = self.db.cursor()
        sql = ""
        for index, info in enumerate(infos):
            if t is 1:
                sql = "INSERT INTO information (url, high, low, title, content, click_num, a_type, k_group, p_date, meta) "\
                      "SELECT %s, %s, %s, %s, %s, 0, %s, 0, %s, %s FROM DUAL "\
                      "WHERE NOT EXISTS (SELECT url FROM information WHERE url=%s)"
                values = (info.getUrl(), info.getHigh(), info.getLow(), info.getTitle(), info.getContent(), \
                          "Article", info.getPDate(), info.getMeta(), info.getUrl())
                cur.execute(sql, values)
                self.db.commit()
                print("[%d]success!" % (index+1))
    def populate(self):
        cur = self.db.cursor()
        cur.execute("INSERT INTO rows(row) VALUES(520)")

    def getArticle(self):
        cur = self.db.cursor()
        cur.execute("SELECT * FROM article")
        row = cur.fetchall()
        return row

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=3300)
