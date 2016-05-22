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


print(sys.stdin.encoding)

try:
    conn = pymysql.connect(host='telegramdb.cctjzlx6kmlc.ap-northeast-1.rds.amazonaws.com', port=3306, user='yongjang', passwd='yongjang', db='telegramdb', charset='utf8')
    print("Database Connection Success!!")
    cur = conn.cursor()
except pymysql.Error as e:
    print ("Error %d: %s" % (e.args[0], e.args[1]))
    sys.exit(1)

TOKEN = '207944330:AAGdpOvswmHangYooE8wBEf1p-vYP2skyL0'
WEBSERVER_DNS = 'ec2-52-196-196-252.ap-northeast-1.compute.amazonaws.com/'

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
              'Jobjang':'Jobjang 서비스 시작하기'
}

imageSelect = types.ReplyKeyboardMarkup(one_time_keyboard=True)  # create the image selection keyboard
imageSelect.add('닭', '고양이')

articleSelect = types.ReplyKeyboardMarkup(one_time_keyboard=True)
articleSelect.add('IT', '사회')

serviceSelect = types.ReplyKeyboardMarkup(one_time_keyboard=True)
serviceSelect.row('/Jobjang')
serviceSelect.row('/help')


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
bot.set_update_listener(listener)  # register listener


# handle the "/start" command
@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    if cid not in knownUsers:
        knownUsers.append(cid)
        userStep[cid] = 0
        bot.send_message(cid, "안녕하세요. 처음 뵙겠습니다.")
        bot.send_message(cid, "사용자 등록이 완료되었습니다.")
        bot.send_message(cid, "사용하실 서비스를 선택하세요.", reply_markup=serviceSelect)
    else:
        bot.send_message(cid, "다시 오신 것을 환영합니다.")
        bot.send_message(cid, "사용하실 서비스를 선택하세요.", reply_markup=serviceSelect)

@bot.message_handler(commands=['Jobjang'])
def command_jobjang(m):
    cid = m.chat.id
    bot.send_message(cid, "당신이 관심있는 분야를 선택하세요.", reply_markup=articleSelectInline)
    userStep[cid] = 100

# help page
@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    help_text = "사용가능한 명령어 목록 입니다.: \n"
    for key in commands:  # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)  # send the generated help page

# broadcasting
@bot.message_handler(commands=['broadcasting'])
def command_help(m):
    for uid in knownUsers:
        cid = uid
        bot.send_message(cid, "Broadcasting 메세지 입니다.")  # send the generated help page
        bot.send_message(cid, "http://www.jobkorea.co.kr/Recruit/GI_Read/17122958?Oem_Code=C1&rPageCode=ST&PageGbn=ST")
        bot.send_message(cid, "http://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=105&oid=421&aid=0002058351")\

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
    text = m.text
    bot.send_message(m.chat.id, "무슨 뜻인지 모르겠습니다. \"" + m.text + "\"\n여기서 사용가능한 명령어를 확인하세요! /help")

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
    cur.execute('SELECT * FROM information WHERE a_Type = \'Article\' ORDER BY click_num DESC;')
    row = cur.fetchall()
    total = len(row)
    entriesURL = []
    if total < 1:
        print('No entries')
    else:
        for record in range(total):
            temp = row[record][1]
            entriesURL.append(temp)
    #### entriesURL에 IT기사 URL 저장 ####
    isFirstShown = -1
    url = ""
    for n in range(entriesURL):
        if cur.execute("SELECT * FROM shown WHERE uid = " + cid + " AND url = \'" + entriesURL[n] + "\';") <1:
            isFirstShown = n
            url = entriesURL[n]
            break;

    if isFirstShown is not -1:
        lastShown[cid] = url
        articleKeyboard = types.InlineKeyboardMarkup(3)
        articleKeyboardDetail = types.InlineKeyboardButton('자세히', callback_data="aDetail")
        articleKeyboardNext = types.InlineKeyboardButton('다른 기사', callback_data="110-1")
        articleKeyboardLink = types.InlineKeyboardButton('링크로 이동', url=WEBSERVER_DNS + "?url=" + url)
        articleKeyboard.row(articleKeyboardDetail, articleKeyboardLink, articleKeyboardNext)
        bot.send_message(cid, WEBSERVER_DNS + "?url=" + url, reply_markup=articleKeyboard)
    else :
        bot.send_message(cid, "아직 준비중입니다.")
        bot.send_message(cid, "어떤 종류의 IT 글을 원하시나요?", reply_markup=step110Keyboard)

"""IT -> 구인정보"""
@bot.callback_query_handler(func=lambda call: call.data == "110-2" and get_user_step(call.from_user.id) == 110)
def step110IT_2(call):
    cid = call.from_user.id
    userStep[cid] = 0
    bot.send_message(cid, WEBSERVER_DNS + "?url=" + "http://www.jobkorea.co.kr//Recruit/GI_Read/17169773?Oem_Code=C1%26rPageCode=ST%26PageGbn=ST")

"""============================================================================================================="""

"""====================================================SET======================================================"""
@bot.callback_query_handler(func=lambda call: call.data == "120-1" and get_user_step(call.from_user.id) == 120)
def step100Social(call):
    cid = call.from_user.id
    #bot.answer_callback_query(call.id, text="사회 기사!!")
    articleKeyboard = types.InlineKeyboardMarkup(3)
    articleKeyboardDetail = types.InlineKeyboardButton('자세히', callback_data="aDetail")
    articleKeyboardNext = types.InlineKeyboardButton('다른 기사', callback_data="120-1")
    articleKeyboardLink = types.InlineKeyboardButton('링크로 이동', url="http://news.naver.com/main/read.nhn?mode=LS2D&mid=shm&sid1=101&sid2=262&oid=003&aid=0007233619")
    articleKeyboard.row(articleKeyboardDetail, articleKeyboardLink, articleKeyboardNext)

    bot.send_message(cid, "http://news.naver.com/main/read.nhn?mode=LS2D&mid=shm&sid1=101&sid2=262&oid=003&aid=0007233619", reply_markup=articleKeyboard)


@bot.callback_query_handler(func=lambda call: call.data == "120-2" and get_user_step(call.from_user.id) == 120)
def step100Social(call):
    cid = call.from_user.id
    #bot.answer_callback_query(call.id, text="사회 기사!!")
    userStep[cid] = 0
    bot.send_message(cid, "http://www.jobkorea.co.kr/Recruit/GI_Read/17126991?Oem_Code=C1&rPageCode=ST&PageGbn=ST")

"""============================================================================================================="""
@bot.callback_query_handler(func=lambda call: call.data == "aDetail")
def step100Social(call):
    cid = call.from_user.id
    #bot.answer_callback_query(call.id, text="사회 기사!!")
    articleKeyboard2 = types.InlineKeyboardMarkup(2)
    if get_user_step(call.from_user.id) == 110:
        userStep[cid] = 110
        articleKeyboardNext = types.InlineKeyboardButton('다른 기사', callback_data="110-1")
        articleKeyboardLink = types.InlineKeyboardButton('링크로 이동', url="http://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=105&oid=421&aid=0002058351")
        articleKeyboard2.row(articleKeyboardLink, articleKeyboardNext)
        bot.send_message(cid, "17일 서울 강남구 코엑스에서 개막한 월드 IT쇼에서 삼성전자와 LG전자 등은 물론 360도 카메라를 만든 씨소 등 IT 중소기업들도 앞다퉈 각사의 VR기기를 선보였다. VR 대중화를 위해 대용량 데이터 전송이 가능한 5G가 필수인 만큼 SK텔레콤과 KT 등 국내 이동통신사 역시 VR 콘텐츠를 대거 선보이며 데이터 전송속도 경쟁을 벌이고 있다.", reply_markup=articleKeyboard2)
    else :
        userStep[cid] = 120
        articleKeyboardNext = types.InlineKeyboardButton('다른 기사', callback_data="120-1")
        articleKeyboardLink = types.InlineKeyboardButton('링크로 이동', url="http://news.naver.com/main/read.nhn?mode=LS2D&mid=shm&sid1=101&sid2=262&oid=003&aid=0007233619")
        articleKeyboard2.row(articleKeyboardLink, articleKeyboardNext)
        bot.send_message(cid, "4월 미국 산업생산은 전월 대비 0.7% 증가해 3개월 만에 반등에 성공했다고 연방준비제도이사회(Fed 연준)가 17일 발표했다.", reply_markup=articleKeyboard2)

bot.polling()
