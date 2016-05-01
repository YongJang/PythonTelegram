from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

def getArticle() :

    html = Request('https://medium.com/browse/b99480981476', headers={'User-Agent':'Mozilla/5.0'})
    webpage = urlopen(html).read()

    soup = BeautifulSoup(webpage)

    bigTitle = soup.find_all("h3")



    for n in range(0,len(bigTitle)):
        linkList = soup.find_all("a", text=bigTitle[n].string)
        print(bigTitle[n].string)

    for n in range(0,len(linkList)):
        print(linkList[n].string)

def Medium_Technology() :
    getArticle()

if __name__ == '__main__' :
    Medium_Technology()
