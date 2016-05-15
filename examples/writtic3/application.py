#!/usr/bin/python
#-*- coding: utf-8 -*-

# 데이터베이스를 위한 라이브러리
import os
import flask
import pymysql
# JSON을 위한 라이브러리
import json
import collections
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
            charset ='utf8'
            )
        cur = self.db.cursor()
        print("connection success!!")
        cur.execute("set names utf8;")
    #cur.execute("DROP TABLE IF EXISTS rows")
    #cur.execute("CREATE TABLE rows(row INT)")
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
                if row[record][0] == category:
                    temp = row[record][1]
                    entries.append(temp)
        return entries
    def getInfo(self):
        '''
        기사, 채용정보를 DB에서 모두 받아온다.
        '''
        cur = self.db.cursor()
        cur.execute("SELECT * FROM information")
        row = cur.fetchall()
        total = len(row)
        entries = []
        if total < 1:
            print('No entries')
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
        return entries

    def setInfo(self, infos, t):
        '''
        기사, 채용정보를 DB에 저장한다.
        TAG는 JSON 타입으로 저장한다.
        '''

        cur = self.db.cursor()
        for index, info in enumerate(infos):
            #tags = json.dumps(info.getTag(), ensure_ascii=False, sort_keys=False, separators=(',', ':'))#.encode('utf-8').decode('utf-8')
            tags = json.dumps(info.getTag(), ensure_ascii=False, sort_keys=False)
            #print(type(info.getUrl()))
            #print(type(tags))
            #print(type(info.getTitle()))
            #print(type(info.getContent()))
            #print(type(info.getPDate()))
            if t is 1:
                if cur.execute("SELECT url from information where url=\'" + info.getUrl() + "\'") < 1:
                    cur.execute("INSERT INTO information(url, tag, title, content ,click_num, a_type, k_group, p_date)" + \
                                "VALUES (\'" + info.getUrl() +"\',\'" + tags + "\',\'" + self.escape(info.getTitle()) + \
                                "\',\'" + self.escape(info.getContent()) + "\', 0, \'Article\', 0, \'" + \
                                info.getPDate() + "\');")
                    self.db.commit()
                    print("[%d]success!" % (index+1))

                else:
                    continue

            else:
                cur.execute("INSERT INTO information(url, tag, title, content, click_num, a_type, k_group, p_date)" + \
                            "VALUES (\'" + info.getUrl +"\',\'" + info.getTag + "\',\'" + info.getTitle + "\',\'" + \
                            info.getContent + "\', 0, \'Article\', 0, \'" + info.getPDate + "\')")
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
