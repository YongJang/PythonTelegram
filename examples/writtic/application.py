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
    score = storage.score()
    return "Are you OK %d!" % score


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
    cur.execute("DROP TABLE IF EXISTS scores")
    #cur.execute("CREATE TABLE scores(score INT)")
    def getInfo(self):
        u"""
        기사, 채용정보를 DB에서 모두 받아온다.
        """
        cur = self.db.cursor()
        cur.execute("SELECT * FROM information")
        row = cur.fetchall()
        total = len(row)
        entries = []
        if total < 1:
            print 'No entries'
        else:
            for record in range(total):
                entry = {}
                entry['url'] = score[record][0]
                entry['tag'] = score[record][1]
                entry['title'] = score[record][2]
                entry['content'] = score[record][3]
                entry['click_num'] = score[record][4]
                entry['a_type'] = score[record][5]
                entry['k_group'] = score[record][6]
                entry['p_data'] = score[record][7]
                entries.append(entry)
            for entry in entries:
                print ' ID: ' + str(entry['pk_aid']) + '\n' +\
                      ' TAG: ' + entry['tag']  + '\n' +\
                      ' Contents: ' + entry['content'] + '\n'
        return entries

    def setInfo(self, info, type):
        u"""
        기사, 채용정보를 DB에 저장한다.
        """
        cur = self.db.cursor()
        for index, info enumerate(info):
            if type is 1:
                cur.execute("INSERT INTO information(url, tag, title, content, click_num, a_type, k_group, p_date)" + \
                            "VALUES (\'" + info.getUrl +"\',\'" + info.getTag + "\',\'" + info.getTitle + "\',\'" + \
                            info.getContent + "\',\'" + info.getClickNum + "\'Article\',\'" + \
                            info.getKGroup + "\',\'" + info.getPDate + "\');")
            else:
                cur.execute("INSERT INTO information(url, tag, title, content, click_num, a_type, k_group, p_date)" + \
                            "VALUES (\'" + info.getUrl +"\',\'" + info.getTag + "\',\'" + info.getTitle + "\',\'" +\
                            info.getContent + "\',\'" + info.getClickNum + "\'Jobkorea\',\'" + \
                            info.getKGroup + "\',\'" + info.getPDate + "\');")
    def populate(self):
        cur = self.db.cursor()
        cur.execute("INSERT INTO scores(score) VALUES(520)")

    def getArticle(self):
        cur = self.db.cursor()
        cur.execute("SELECT * FROM article")
        row = cur.fetchall()
        return row

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=3300)
