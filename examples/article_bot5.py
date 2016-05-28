#!/usr/bin/python
#-*- coding: utf-8 -*-
"""
This is a detailed example using almost every command of the API
참고하고 있는 사이트
https://github.com/eternnoir/pyTelegramBotAPI/issues?utf8=%E2%9C%93&q=to_dic
https://github.com/eternnoir/pyTelegramBotAPI/releases/tag/2.0.5
InlineKeyboardButton : https://github.com/eternnoir/pyTelegramBotAPI/issues/130
CallbackQuery : https://github.com/eternnoir/pyTelegramBotAPI/pull/148/commits/4cb8f14a20c77ce2662ab343b27f4118181293fa
"""

import telebot
from telebot import types
import time
from urllib.request import Request, urlopen
import requests
from io import BytesIO
from PIL import Image
import json
import pymysql
import sys
import feedparser
import urllib.parse




print(sys.stdin.encoding)

try:
    conn = pymysql.connect(host='telegramdb.cctjzlx6kmlc.ap-northeast-1.rds.amazonaws.com', port=3306, user='yongjang', passwd='yongjang', db='telegramdb', charset='utf8', use_unicode=False, init_command='SET NAMES UTF8')
    print("Database Connection Success!!")
    cur = conn.cursor()
except pymysql.Error as e:
    print ("Error %d: %s" % (e.args[0], e.args[1]))
    sys.exit(1)
# @yongjang_bot
#TOKEN = '207944330:AAGdpOvswmHangYooE8wBEf1p-vYP2skyL0'
# @JobJangBot
TOKEN = '207840488:AAEf42L9r0V2tHrX1lVm0QTRnj1e6m5y5bQ'
WEBSERVER_DNS = 'TelegramRedirect-982942058.ap-northeast-1.elb.amazonaws.com/'

# uid 가져오기
cur.execute("SELECT * FROM users")
row = cur.fetchall()
knownUsers = []
total = len(row)
if total < 1:
    print('no users')
else:
    for record in range(total):
        temp = row[record][0]
        knownUsers.append(temp)

######

userStep = {}
lastShown = {}

commands = {
              'start': '봇 사용을 시작합니다.',
              'help': '사용 가능한 명령어들을 봅니다.',
              'broadcasting':'이 봇을 사용하는 모든 유저에게 메세지를 전달합니다.',
              'getImage': '이미지를 가져옵니다.',
              'JobJang':'잡장 서비스 시작하기',
              'keyword':'키워드검색 서비스 시작하기'
}

imageSelect = types.ReplyKeyboardMarkup(one_time_keyboard=True)
imageSelect.add('닭', '고양이')

articleSelect = types.ReplyKeyboardMarkup(one_time_keyboard=True)
articleSelect.add('IT', '사회')

serviceSelect = types.ReplyKeyboardMarkup(one_time_keyboard=True)
serviceSelect.row('/잡장')
serviceSelect.row('/키워드검색')
serviceSelect.row('/도움말','/재시작')


# 타인한테 전달하는 버튼
# inlineButton1 = types.InlineKeyboardButton('1', switch_inline_query="a")
# inlineButton2 = types.InlineKeyboardButton('2', switch_inline_query="b")
articleSelectInline = types.InlineKeyboardMarkup(2)
step100Button1 = types.InlineKeyboardButton('IT', callback_data="100-1")
step100Button2 = types.InlineKeyboardButton('사회', callback_data="100-2")
#step100Button3 = types.InlineKeyboardButton('친구에게 봇 추천하기', switch_inline_query="<-- [클릭] 이건 짱 좋은 봇입니다. 기사도 가져다주고 구인 정보도 가져다줌")
#articleSelectInline.add(step100Button1, step100Button2, step100Button3)
articleSelectInline.add(step100Button1, step100Button2)


step110Keyboard = types.InlineKeyboardMarkup(2)
step110Button1 = types.InlineKeyboardButton('기사', callback_data="110-1")
step110Button2 = types.InlineKeyboardButton('구인 정보', callback_data="110-2")
step110Keyboard.add(step110Button1, step110Button2)

step120Keyboard = types.InlineKeyboardMarkup(2)
step120Button1 = types.InlineKeyboardButton('기사', callback_data="120-1")
step120Button2 = types.InlineKeyboardButton('구인 정보', callback_data="120-2")
step120Keyboard.add(step120Button1, step120Button2)


""" 예제 결과화면 만들기 위해 잠시 수정
articleKeyboard = types.InlineKeyboardMarkup(3)
articleKeyboard2 = types.InlineKeyboardMarkup(2)
articleKeyboardDetail = types.InlineKeyboardButton('자세히', callback_data="aDetail")
articleKeyboardNext = types.InlineKeyboardButton('다른 기사', callback_data="aNext")
articleKeyboardLink = types.InlineKeyboardButton('링크로 이동', callback_data="aLink")

articleKeyboard.row(articleKeyboardDetail, articleKeyboardLink, articleKeyboardNext)
articleKeyboard2.row(articleKeyboardLink, articleKeyboardNext)
"""

hideBoard = types.ReplyKeyboardHide()
forceBoard = types.ForceReply()

def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        if uid not in knownUsers:
            knownUsers.append(uid)
            cur.execute("INSERT INTO users (PK_uid, step) VALUES (\'" + str(uid) + "\',\'0\')" )
            conn.commit()
        userStep[uid] = 0
        print ("새로운 시작 \"/start\"")
        return 0


def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        if m.content_type == 'text':
            print (str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text)

bot = telebot.TeleBot(TOKEN)
bot.set_update_listener(listener)  # listener 등록

@bot.message_handler(commands=['start','재시작'])
def command_start(m):
    cid = m.chat.id
    try:
        if cid not in knownUsers:
            knownUsers.append(cid)
            userStep[cid] = 0
            bot.send_message(cid, m.chat.first_name + "님 안녕하세요. 처음 뵙겠습니다.")
            bot.send_message(cid, "사용자 등록이 완료되었습니다.")
            bot.send_message(cid, "사용하실 서비스를 선택하세요.", reply_markup=serviceSelect)
        else:
            userStep[cid] = 0
            bot.send_message(cid, m.chat.first_name + "님 다시 오신 것을 환영합니다.")
            bot.send_message(cid, "사용하실 서비스를 선택하세요.", reply_markup=serviceSelect)
    except Exception as e:
	        print(e)

@bot.message_handler(commands=['잡장','JobJang'])
def command_jobjang(m):
    cid = m.chat.id
    if get_user_step(cid) == 110:
        bot.send_message(cid, "어떤 종류의 IT 글을 원하시나요?", reply_markup=step110Keyboard)
    elif get_user_step(cid) == 120:
        bot.send_message(cid, "어떤 종류의 사회 글을 원하시나요?", reply_markup=step120Keyboard)
    else :
        bot.send_message(cid, "분야별로 필요한 정보를 받으실 수 있습니다.")
        bot.send_message(cid, "당신이 관심있는 분야를 선택하세요.", reply_markup=articleSelectInline, parse_mode='Markdown')
        userStep[cid] = 100

@bot.message_handler(commands=['키워드검색','keyword'])
def command_jobnews(m):
    cid = m.chat.id
    userStep[cid] = 200
    text = "검색하실 키워드를 입력하세요."
    bot.send_message(cid, text, reply_markup=forceBoard)


# help page
@bot.message_handler(commands=['도움말','help'])
def command_help(m):
    cid = m.chat.id
    help_text = "사용가능한 명령어 목록 입니다.: \n"
    for key in commands:
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)

# broadcasting
@bot.message_handler(commands=['broadcasting'])
def command_broadcast(m):
    sender = m.chat.first_name
    for uid in knownUsers:
        cid = uid
        bot.send_message(cid, sender + "님의 Broadcasting 메세지 입니다.")

@bot.message_handler(commands=['getImage'])
def command_image(m):
    cid = m.chat.id
    bot.send_message(cid, "이미지를 선택하세요.", reply_markup=imageSelect)
    userStep[cid] = 1


@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 1)
def msg_image_select(m):
    cid = m.chat.id
    text = m.text
    bot.send_chat_action(cid, 'typing')
    if text == "닭":
        bot.send_photo(cid, open('rooster.jpg', 'rb'),
                       reply_markup=hideBoard)
        userStep[cid] = 0
    elif text == "고양이":
        bot.send_photo(cid, open('kitten.jpg', 'rb'), reply_markup=hideBoard)
        userStep[cid] = 0
    else:
        url = "http://runezone.com/imagehost/images/5741/Cute-Kitten.jpg"
        #imgdata = urlopen(url).read()
        #response = Request(url, headers={'User-Agent':'Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)'})
        req = Request(url, headers={'User-Agent':'Mozilla/5.0'})
        response = urlopen(req)
        #img = Image.open(BytesIO(urlopen(response).read()))
        img = response.read()

        """
        에러 발생(미해결)
        Photo has unsupported extension. Use one of .jpg, .jpeg, .gif, .png, .tif or .bmp
        """
        bot.send_photo(cid, img, reply_markup = hideBoard)
        bot.send_message(cid, "Success!!")
        bot.send_message(cid, "Please try again")


@bot.message_handler(func=lambda message: message.text == "hi")
def command_text_hi(m):
    bot.send_message(m.chat.id, "안녕하세요!")


# 디폴트
@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    cid = m.chat.id
    step = get_user_step(cid)
    if step == 200:
        command_News_Search(m)
    else:
        text = m.text
        bot.send_message(m.chat.id, "무슨 뜻인지 모르겠습니다. \"" + m.text + "\"\n여기서 사용가능한 명령어를 확인하세요! /help")
#@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 200 , content_types=['text'])
def command_News_Search(m):
    cid = m.chat.id
    userStep[cid] = 0
    keyword = m.text
    d = feedparser.parse('http://newssearch.naver.com/search.naver?where=rss&query=' + urllib.parse.quote(keyword.encode("utf-8")) + '&field=0')
    sendText = ""
    isFirstShown = -1
    url = ""
    for post in d.entries:
        if cur.execute("SELECT * FROM shown WHERE uid = " + str(cid) + " AND url = \'" + post.link + "\';") <1:
            isFirstShown = 1
            url = post
            break;
    if isFirstShown is not -1:
        sendText = keyword + "에 대한 검색 결과 입니다.\n[제목] : " + url.title + "\n[키워드가 포함되어 있는 문장] : " + url.summary + "\n[발간일자] : " + url.published + "\n" + url.link
        if len(sendText) > 2047:
            sendText = sendText[0:2040]
        cur.execute("INSERT INTO shown (uid, url) VALUES (\'" + str(cid) +"\',\'" + url.link + "\');")
        conn.commit()
            KeywordKeyboard = types.InlineKeyboardMarkup(3)
            KeywordButton1 = types.InlineKeyboardButton('같은 키워드로 다시 검색', callback_data="201?"+keyword)
            KeywordButton2 = types.InlineKeyboardButton('계속 검색', callback_data="202")
            KeywordButton3 = types.InlineKeyboardButton('처음으로', callback_data="203")
            KeywordButton4 = types.InlineKeyboardButton('공유하기', switch_inline_query=""+sendText)
            KeywordKeyboard.row(KeywordButton1)
            KeywordKeyboard.row(KeywordButton2)
            KeywordKeyboard.row(KeywordButton3,KeywordButton4)
        bot.send_message(cid, sendText, parse_mode='HTML',reply_markup=KeywordKeyboard)
    else :
        bot.send_message(cid, "검색 결과를 찾을 수 없습니다.")



# 여기서 부터 callback_query 핸들러
"""====================================================SET======================================================"""
@bot.callback_query_handler(func=lambda call: call.data == "100-1" and get_user_step(call.from_user.id) == 100)
def step100IT(call):
    cid = call.from_user.id
    userStep[cid] = 110
    bot.send_message(cid, "어떤 종류의 IT 글을 원하시나요?", reply_markup=step110Keyboard)


@bot.callback_query_handler(func=lambda call: call.data == "100-2" and get_user_step(call.from_user.id) == 100)
def step100Social(call):
    cid = call.from_user.id
    userStep[cid] = 120
    bot.send_message(cid, "어떤 종류의 사회 글을 원하시나요?", reply_markup=step120Keyboard)

"""============================================================================================================="""

"""====================================================SET======================================================"""
"""IT -> 기사"""
@bot.callback_query_handler(func=lambda call: call.data == "110-1" and get_user_step(call.from_user.id) == 110)
def step110IT_1(call):
    cid = call.from_user.id
    cur.execute("SELECT * FROM information WHERE high = \'IT\' ORDER BY click_num DESC;")
    row = cur.fetchall()
    total = len(row)
    entriesURL = []
    if total < 1:
        print('No entries')
    else:
        for record in range(total):
            temp = row[record][1].decode('utf8', 'surrogatepass')
            entriesURL.append(temp)
    #### entriesURL에 IT기사 URL 저장 ####
    isFirstShown = -1
    url = ""
    for n in range(len(entriesURL)):
        if cur.execute("SELECT * FROM shown WHERE uid = " + str(cid) + " AND url = \'" + entriesURL[n] + "\';") <1:
            isFirstShown = n
            url = entriesURL[n]
            break;

    if isFirstShown is not -1:
        lastShown[cid] = url
        cur.execute("INSERT INTO shown (uid, url) VALUES (\'" + str(cid) +"\',\'" + url + "\');")
        conn.commit()
        articleKeyboard = types.InlineKeyboardMarkup(3)
        articleKeyboardDetail = types.InlineKeyboardButton('자세히', callback_data="aDetail")
        articleKeyboardNext = types.InlineKeyboardButton('다른 기사', callback_data="110-1")
        articleKeyboardLink = types.InlineKeyboardButton('링크로 이동', url=WEBSERVER_DNS + "?url=" + url + "&tb=information")
        articleKeyboard.row(articleKeyboardDetail, articleKeyboardLink, articleKeyboardNext)
        bot.send_message(cid, WEBSERVER_DNS + "?url=" + url + "&tb=information", reply_markup=articleKeyboard)
    else :
        bot.send_message(cid, "아직 준비중입니다.")
        bot.send_message(cid, "어떤 종류의 IT 글을 원하시나요?", reply_markup=step110Keyboard)

"""IT -> 구인정보"""
@bot.callback_query_handler(func=lambda call: call.data == "110-2" and get_user_step(call.from_user.id) == 110)
def step110IT_2(call):
    cid = call.from_user.id
    cur.execute("SELECT * FROM jobs WHERE aType = \'Job\' ORDER BY click_num DESC;")
    row = cur.fetchall()
    total = len(row)
    jobsURL = []
    if total < 1:
        print('No entries')
    else:
        for record in range(total):
            temp = row[record][1].decode('utf8', 'surrogatepass')
            jobsURL.append(temp)

    isFirstShown = -1
    url = ""
    for n in range(len(jobsURL)):
        if cur.execute("SELECT * FROM shown WHERE uid = " + str(cid) + " AND url = \'" + jobsURL[n] + "\';") <1:
            isFirstShown = n
            url = jobsURL[n]
            break;
    if isFirstShown is not -1:
        lastShown[cid] = url
        cur.execute("INSERT INTO shown (uid, url) VALUES (\'" + str(cid) +"\',\'" + url + "\');")
        conn.commit()
        articleKeyboard = types.InlineKeyboardMarkup(2)
        articleKeyboardNext = types.InlineKeyboardButton('다른 정보', callback_data="110-2")
        articleKeyboardLink = types.InlineKeyboardButton('링크로 이동', url=WEBSERVER_DNS + "?url=" + url + "&tb=jobs")
        articleKeyboard.row(articleKeyboardLink, articleKeyboardNext)
        bot.send_message(cid, WEBSERVER_DNS + "?url=" + url + "&tb=jobs", reply_markup=articleKeyboard)
    else :
        bot.send_message(cid, "아직 준비중입니다.")
        bot.send_message(cid, "어떤 종류의 IT 글을 원하시나요?", reply_markup=step110Keyboard)

"""============================================================================================================="""

"""====================================================SET======================================================"""
"""사회 -> 기사"""
@bot.callback_query_handler(func=lambda call: call.data == "120-1" and get_user_step(call.from_user.id) == 120)
def step120Social_1(call):
    cid = call.from_user.id
    cur.execute("SELECT * FROM information WHERE high = \'경제\' ORDER BY click_num DESC;")
    row = cur.fetchall()
    total = len(row)
    entriesURL = []
    if total < 1:
        print('No entries')
    else:
        for record in range(total):
            temp = row[record][1].decode('utf8', 'surrogatepass')
            entriesURL.append(temp)
    #### entriesURL에 IT기사 URL 저장 ####
    isFirstShown = -1
    url = ""
    for n in range(len(entriesURL)):
        if cur.execute("SELECT * FROM shown WHERE uid = " + str(cid) + " AND url = \'" + entriesURL[n] + "\';") <1:
            isFirstShown = n
            url = entriesURL[n]
            break;

    if isFirstShown is not -1:
        lastShown[cid] = url
        cur.execute("INSERT INTO shown (uid, url) VALUES (\'" + str(cid) +"\',\'" + url + "\');")
        conn.commit()
        articleKeyboard = types.InlineKeyboardMarkup(3)
        articleKeyboardDetail = types.InlineKeyboardButton('자세히', callback_data="aDetail")
        articleKeyboardNext = types.InlineKeyboardButton('다른 기사', callback_data="120-1")
        articleKeyboardLink = types.InlineKeyboardButton('링크로 이동', url=WEBSERVER_DNS + "?url=" + url + "&tb=information")
        articleKeyboard.row(articleKeyboardDetail, articleKeyboardLink, articleKeyboardNext)
        bot.send_message(cid, WEBSERVER_DNS + "?url=" + url + "&tb=information", reply_markup=articleKeyboard)
    else :
        bot.send_message(cid, "아직 준비중입니다.")
        bot.send_message(cid, "어떤 종류의 사회 글을 원하시나요?", reply_markup=step120Keyboard)

"""사회 -> 구인정보"""
@bot.callback_query_handler(func=lambda call: call.data == "120-2" and get_user_step(call.from_user.id) == 120)
def step120Social_2(call):
    cid = call.from_user.id
    cur.execute("SELECT * FROM society WHERE aType = \'Job\' ORDER BY click_num DESC;")
    row = cur.fetchall()
    total = len(row)
    jobsURL = []
    if total < 1:
        print('No entries')
    else:
        for record in range(total):
            temp = row[record][1].decode('utf8', 'surrogatepass')
            jobsURL.append(temp)

    isFirstShown = -1
    url = ""
    for n in range(len(jobsURL)):
        if cur.execute("SELECT * FROM shown WHERE uid = " + str(cid) + " AND url = \'" + jobsURL[n] + "\';") <1:
            isFirstShown = n
            url = jobsURL[n]
            break;
    if isFirstShown is not -1:
        lastShown[cid] = url
        cur.execute("INSERT INTO shown (uid, url) VALUES (\'" + str(cid) +"\',\'" + url + "\');")
        conn.commit()
        articleKeyboard = types.InlineKeyboardMarkup(2)
        articleKeyboardNext = types.InlineKeyboardButton('다른 정보', callback_data="120-2")
        articleKeyboardLink = types.InlineKeyboardButton('링크로 이동', url=WEBSERVER_DNS + "?url=" + url + "&tb=society")
        articleKeyboard.row(articleKeyboardLink, articleKeyboardNext)
        bot.send_message(cid, WEBSERVER_DNS + "?url=" + url + "&tb=society", reply_markup=articleKeyboard)
    else :
        bot.send_message(cid, "아직 준비중입니다.")
        bot.send_message(cid, "어떤 종류의 사회 글을 원하시나요?", reply_markup=step120Keyboard)

"""============================================================================================================="""
"""====================================================SET======================================================"""
@bot.callback_query_handler(func=lambda call: call.data[:4] == "201?")
def step201(call):
    cid = call.from_user.id
    userStep[cid] = 0
    keyword = str(call.data[4:len(call.data)])
    d = feedparser.parse('http://newssearch.naver.com/search.naver?where=rss&query=' + urllib.parse.quote(keyword.encode("utf-8")) + '&field=0')
    sendText = ""
    isFirstShown = -1
    url = ""
    for post in d.entries:
        if cur.execute("SELECT * FROM shown WHERE uid = " + str(cid) + " AND url = \'" + post.link + "\';") <1:
            isFirstShown = 1
            url = post
            break;
    if isFirstShown is not -1:
        sendText = keyword + "에 대한 검색 결과 입니다.\n[제목] : " + url.title + "\n[키워드가 포함되어 있는 문장] : " + url.summary + "\n[발간일자] : " + url.published + "\n" + url.link
        if len(sendText) > 2047:
            sendText = sendText[0:2040]
        cur.execute("INSERT INTO shown (uid, url) VALUES (\'" + str(cid) +"\',\'" + url.link + "\');")
        conn.commit()
        KeywordKeyboard = types.InlineKeyboardMarkup(3)
        KeywordButton1 = types.InlineKeyboardButton('같은 키워드로 다시 검색', callback_data="201?"+keyword)
        KeywordButton2 = types.InlineKeyboardButton('계속 검색', callback_data="202")
        KeywordButton3 = types.InlineKeyboardButton('처음으로', callback_data="203")
        KeywordButton4 = types.InlineKeyboardButton('공유하기', switch_inline_query=""+sendText)
        KeywordKeyboard.row(KeywordButton1)
        KeywordKeyboard.row(KeywordButton2)
        KeywordKeyboard.row(KeywordButton3,KeywordButton4)
        bot.send_message(cid, sendText, parse_mode='HTML',reply_markup=KeywordKeyboard)
    else :
        bot.send_message(cid, "검색 결과를 찾을 수 없습니다.")

@bot.callback_query_handler(func=lambda call: call.data == "202")
def step202(call):
    cid = call.from_user.id
    userStep[cid] = 200
    text = "검색하실 키워드를 입력하세요."
    bot.send_message(cid, text, reply_markup=forceBoard)

@bot.callback_query_handler(func=lambda call: call.data == "203")
def step203(call):
    cid = call.from_user.id
    bot.send_message(cid, "사용하실 서비스를 선택하세요.", reply_markup=serviceSelect)
"""============================================================================================================="""
@bot.callback_query_handler(func=lambda call: call.data == "aDetail")
def stepDetail(call):
    cid = call.from_user.id
    url = lastShown[cid]
    #bot.answer_callback_query(call.id, text="사회 기사!!")
    articleKeyboard2 = types.InlineKeyboardMarkup(2)

#"""IT -> 기사 -> 자세히"""
    try:
        if get_user_step(call.from_user.id) == 110:
            userStep[cid] = 110
            cur.execute("SELECT * FROM information WHERE high = \'IT\' AND url = \'" + url + "\';")
            row = cur.fetchall()
            total = len(row)
            detail = ""
            if total < 1:
                print('No entries')
            else:
                for record in range(total):
                    temp = row[record][5].decode('utf8', 'surrogatepass')
                    detail = temp
            if len(detail)>2047:
                detail = detail[0:2040]
                detil = detail +"..."
            articleKeyboardNext = types.InlineKeyboardButton('다른 기사', callback_data="110-1")
            articleKeyboardLink = types.InlineKeyboardButton('링크로 이동', url=WEBSERVER_DNS + "?url=" + url + "&tb=information")
            articleKeyboard2.row(articleKeyboardLink, articleKeyboardNext)
            bot.send_message(cid, detail, reply_markup=articleKeyboard2)

    #"""사회 -> 기사 -> 자세히"""

        else :
            userStep[cid] = 120
            cur.execute("SELECT * FROM information WHERE high = \'경제\' AND url = \'" + url + "\';")
            row = cur.fetchall()
            total = len(row)
            detail = ""
            if total < 1:
                print('No entries')
            else:
                for record in range(total):
                    temp = row[record][5].decode('utf8', 'surrogatepass')
                    detail = temp
            if len(detail)>2047:
                detail = detail[0:2040]
                detil = detail +"..."
            articleKeyboardNext = types.InlineKeyboardButton('다른 기사', callback_data="120-1")
            articleKeyboardLink = types.InlineKeyboardButton('링크로 이동', url=WEBSERVER_DNS + "?url=" + url + "&tb=information")
            articleKeyboard2.row(articleKeyboardLink, articleKeyboardNext)
            bot.send_message(cid, detail, reply_markup=articleKeyboard2)
    except Exception as e:
    	        print(e)

bot.polling()
