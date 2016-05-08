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
    w = storage.getTags(u"IT")
    for e in w:
        print "keyword: " + e[0]
    result = crawling.getContent(crawling.getNews(1), w);
    for index, e in enumerate(result):
        resultText = '[%d개]' % (index+1) + e.getTag() + e.getPDate()
        print resultText
    #storage.setInfo(result, 1)
    #entries = storage.getInfo()
    #for entry in entries:
    #    print ' URL: ' + str(entry.getUrl()) + '\n' +\
    #          ' TAG: ' + str(entry.getTag())  + '\n' +\
    #          ' title: ' + str(entry.getTitle()) + '\n'
    #time.sleep(5)

def main():
  unittest.main()

if __name__ == "__main__":
  main()
