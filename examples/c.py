from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

def getArticle() :

    html = Request('https://medium.com/browse/b99480981476;', headers={'User-Agent':'Mozilla/5.0'})
    webpage = urlopen(html).read()

    soup = BeautifulSoup(webpage)

    hoi = soup.find("h3")

    numbers=[]

    for n in range(1,4):
        strV = str(n)
        numbers.append(strV)

    print('!!')
    print(hoi.string + "results")
    print(" ".join(numbers))

def Medium_Technology() :
    getArticle()

if __name__ == '__main__' :
    Medium_Technology()
