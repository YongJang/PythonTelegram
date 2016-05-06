#-*- coding: utf-8 -*-
import os
import flask
import pymysql

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
    #cur.execute("DROP TABLE IF EXISTS scores")
    #cur.execute("CREATE TABLE scores(score INT)")


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
