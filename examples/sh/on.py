from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

def getPost() :

    html = Request('http://www.onoffmix.com/event?s=IT', headers={'User-Agent':'Mozilla/5.0'})
    webpage = urlopen(html).read()
    soup = BeautifulSoup(webpage)
    event = soup.find('a', class_="eventLink")
    for i in event:
        print (event[i].get("title"))

def Medium_Technology() :
    getPost()

if __name__ == '__main__' :
    Medium_Technology()
