# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.

import telebot

API_TOKEN = '207944330:AAGdpOvswmHangYooE8wBEf1p-vYP2skyL0'

bot = telebot.TeleBot(API_TOKEN)

#LOTTO#
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

# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, "Lotto numbers\n"+hoi.string + "results"+" ".join(numbers)+'Bonus_number: '+bonus)


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)

bot.polling()
