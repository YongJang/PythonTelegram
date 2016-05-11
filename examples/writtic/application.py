#!/usr/bin/python
#-*- coding: utf-8 -*-

# 데이터베이스를 위한 라이브러리
import os
import flask
import pymysql
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
            port = int(os.getenv('MYSQL_PORT_3306_TCP_PORT', '3306'))
            )

        cur = self.db.cursor()
        cur.execute("set names utf8")
    #cur.execute("DROP TABLE IF EXISTS rows")
    #cur.execute("CREATE TABLE rows(row INT)")
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
        cur.close()
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
        cur.close()
        return entries

    def setInfo(self, infos, type):
        '''
        기사, 채용정보를 DB에 저장한다.
        '''
        cur = self.db.cursor()
        for index, info in enumerate(infos):
            if type is 1:
                cur.execute("INSERT INTO information(url, tag, title, content, click_num, a_type, k_group, p_date)" + \
                            "VALUES (\'" + str(info.getUrl()) +"\',\'" + str(info.getTag()) + "\',\'" + str(info.getTitle()) + "\',\'" + \
                            str(info.getContent()) + "\', 0, \'Article\', 0, \'" + str(info.getPDate()) + "\')")
            else:
                cur.execute("INSERT INTO information(url, tag, title, content, click_num, a_type, k_group, p_date)" + \
                            "VALUES (\'" + info.getUrl +"\',\'" + info.getTag + "\',\'" + info.getTitle + "\',\'" + \
                            info.getContent + "\', 0, \'Article\', 0, \'" + info.getPDate + "\')")
        cur.close()
    def populate(self):
        cur = self.db.cursor()
        cur.execute("INSERT INTO rows(row) VALUES(520)")

    def getArticle(self):
        cur = self.db.cursor()
        cur.execute("SELECT * FROM article")
        row = cur.fetchall()
        return row
    def __del__(self):
        if self.db:
            self.db.cursor().close()
            self.db.close()

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=3300)
