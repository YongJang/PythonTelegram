from bs4 import BeautifulSoup
import urllib2

def crawling():
        url="http://www.utexas.edu/world/univ/alpha/"
        page=urllib2.urlopen(url)
        soup = BeautifulSoup(page.read())


if __name__ == '__main__':
    crawling()
