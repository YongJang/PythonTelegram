from bs4 import BeautifulSoup
import urllib.request

def getArticle() :
    html = urllib.request.urlopen('https://medium.com/browse/b99480981476;')

    soup = BeautifulSoup(html)

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
