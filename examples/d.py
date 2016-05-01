from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

def getArticle() :

    html = Request('http://news.naver.com/main/search/search.nhn?query=%C0%CE%B0%F8%C1%F6%B4%C9&st=news.all&q_enc=EUC-KR&r_enc=UTF-8&r_format=xml&rp=none&sm=all.basic&ic=all&so=rel.dsc&detail=0&pd=1&r_cluster2_start=11&r_cluster2_display=10&start=11&display=5&page=1', headers={'User-Agent':'Mozilla/5.0'})
    webpage = urlopen(html).read()

    soup = BeautifulSoup(webpage)

    bigTitle = soup.find_all(class_="tit")



    for n in range(0,len(bigTitle)):
        if "\"" not in bigTitle[n]:
            print(bigTitle[n].string)
        else:
            print(bigTitle[n])


def Medium_Technology() :
    getArticle()

if __name__ == '__main__' :
    Medium_Technology()
