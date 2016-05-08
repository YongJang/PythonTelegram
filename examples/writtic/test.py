#-*- coding: utf-8 -*-
import unittest
import time
from application import Storage
from webCrawler import Crawling
from jobjangDTO import Information

class TestSuite(unittest.TestCase):
  def test(self):
    storage = Storage()
    crawling = Crawling()
    #storage.populate()
    #score = storage.getArticle()
    w = storage.getTags('IT')
    result = crawling.getContent(crawling.getNews(1), w);
    storage.setInfo(result, 1)
    entries = storage.getInfo()
    for entry in entries:
        print ' URL: ' + str(entry['url']) + '\n' +\
              ' TAG: ' + entry['tag']  + '\n' +\
              ' Contents: ' + entry['content'] + '\n'
    time.sleep(5)

def main():
  unittest.main()

if __name__ == "__main__":
  main()
