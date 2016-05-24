#!/usr/bin/python
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
        #getNews에 들어가는 매개변수는 기사를 긁어오는 범위다. (15면 15일치 기사들을 모두 긁음.)
        results = crawling.getContent(crawling.getNews(15), storage.getTags('IT'));
        for index, result in enumerate(results):
            r = Information()
            r = result
            resultText = '[%d개] ' % (index+1) + r.toString() + ' From Crawling'
            print(resultText)
        storage.setInfo(results, 1)
        entries = storage.getInfo()
        for index, entry in enumerate(entries):
            e = entry
            print('[%d개] ' % (index+1) + e.toString() + ' From DB')
            #time.sleep(5)

def main():
    unittest.main()

if __name__ == "__main__":
    main()
