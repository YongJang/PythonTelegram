from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

def getPost() :

    html = Request('http://www.jobkorea.co.kr/net/Starter/Recruit/SS/engineering?rOrderTab=10#JobList', headers={'User-Agent':'Mozilla/5.0'})
    webpage = urlopen(html).read()
    soup = BeautifulSoup(webpage)
    info_title = soup.find_all("a" ,class_="emp1")
    page = soup.find_all("div" ,class_="lgiSec lgiPagination lgiPagination1")
    page_array = []
    for countpage in page:
        page_array.append([countpage.get_text()])
        print(page_array)


    for i in info_title:
        print (i.get("title"))

def Medium_Technology() :
    getPost()

if __name__ == '__main__' :
    Medium_Technology()
