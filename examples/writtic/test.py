#-*- coding: utf-8 -*-
import unittest
from application import Storage

class TestSuite(unittest.TestCase):
  def test(self):
    storage = Storage()
    #storage.populate()
    score = storage.getArticle()
    total = len(score)
    entries = []
    if total < 1:
        print 'No entries'
    else:
        for record in range(total):
            entry = {}
            entry['PK_aid'] = score[record][0]
            entry['url'] = score[record][1]
            entry['tag'] = score[record][2]
            entry['content'] = score[record][3]
            entry['click_num'] = score[record][4]
            entry['aType'] = score[record][5]
            entry['k_group'] = score[record][6]
            entry['pData'] = score[record][7]
            entries.append(entry)
        for entry in entries:
            print ' ID: ' + str(entry['PK_aid']) + '\n' +\
                  ' TAG: ' + entry['tag']  + '\n' +\
                  ' Contents: ' + entry['content'] + '\n'
                  #self.failIf(score != 520)

def main():
  unittest.main()

if __name__ == "__main__":
  main()
