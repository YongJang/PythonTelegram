from bs4 import BeautifulSoup
import urllib.request

html = urllib.request.urlopen('http://www.nlotto.co.kr/common.do?method=main&#8217;')

soup = BeautifulSoup(html)

hoi = soup.find("span", id="lottoDrwNo")

numbers=[]

for n in range(1,7):
    strV ="drwtNo" + str(n)
    first = soup.find('img', id=strV)['alt']
    numbers.append(first)

bonus = soup.find('img', id="bnusNo")['alt']

print('Lotto numbers')
print(hoi.string + "results")
print(" ".join(numbers))
print('Bonus_number: '+bonus)
