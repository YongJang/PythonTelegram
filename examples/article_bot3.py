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

userStep = {}  # so they won't reset every time the bot restarts

commands = {  # command description used in the "help" command
              'start': '봇 사용을 시작합니다.',
              'help': '사용 가능한 명령어들을 봅니다.',
              #'sendLongText': 'A test using the \'send_chat_action\' command',
              'broadcasting':'이 봇을 사용하는 모든 유저에게 메세지를 전달합니다.',
              'getImage': '이미지를 가져옵니다.',
              'getArticle': '네이버 기사 크롤링 테스트'
}

imageSelect = types.ReplyKeyboardMarkup(one_time_keyboard=True)  # create the image selection keyboard
imageSelect.add('닭', '고양이')

articleSelect = types.ReplyKeyboardMarkup(one_time_keyboard=True)
articleSelect.add('IT', '사회')

serviceSelect = types.ReplyKeyboardMarkup(one_time_keyboard=True)
serviceSelect.row('Jobjang')


# 타인한테 전달하는 버튼
# inlineButton1 = types.InlineKeyboardButton('1', switch_inline_query="a")
# inlineButton2 = types.InlineKeyboardButton('2', switch_inline_query="b")
articleSelectInline = types.InlineKeyboardMarkup(2)
step100Button1 = types.InlineKeyboardButton('IT', callback_data="100-1")
step100Button2 = types.InlineKeyboardButton('사회', callback_data="100-2")
step100Button3 = types.InlineKeyboardButton('친구에게 봇 추천하기', switch_inline_query="<-- [클릭] 이건 짱 좋은 봇입니다. 기사도 가져다주고 구인 정보도 가져다줌")
articleSelectInline.add(step100Button1, step100Button2, step100Button3)


step110Keyboard = types.InlineKeyboardMarkup(2)
step110Button1 = types.InlineKeyboardButton('기사', callback_data="110-1")
step110Button2 = types.InlineKeyboardButton('구인 정보', callback_data="110-2")
step110Keyboard.add(step110Button1, step110Button2)

step120Keyboard = types.InlineKeyboardMarkup(2)
step120Button1 = types.InlineKeyboardButton('기사', callback_data="120-1")
step120Button2 = types.InlineKeyboardButton('구인 정보', callback_data="120-2")
step120Keyboard.add(step120Button1, step120Button2)


hideBoard = types.ReplyKeyboardHide()  # if sent as reply_markup, will hide the keyboard


# error handling if user isn't known yet
# (obsolete once known users are saved to file, because all users
#   had to use the /start command and are therefore known to the bot)
def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        knownUsers.append(uid)
        cur.execute("INSERT INTO users (PK_uid, step) VALUES (\'" + str(uid) + "\',\'0\')" )
        conn.commit()
        userStep[uid] = 0
        print ("New user detected, who hasn't used \"/start\" yet")
        return 0


# only used for console output now
def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        if m.content_type == 'text':
            # print the sent message to the console
            print (str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text)


bot = telebot.TeleBot(TOKEN)
bot.set_update_listener(listener)  # register listener


# handle the "/start" command
@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    if cid not in knownUsers:  # if user hasn't used the "/start" command yet:
        knownUsers.append(cid)  # save user id, so you could brodcast messages to all users of this bot later
        userStep[cid] = 0  # save user id and his current "command level", so he can use the "/getImage" command
        bot.send_message(cid, "안녕하세요. 처음 뵙겠습니다.")
        bot.send_message(cid, "사용자 등록이 완료되었습니다.")
        bot.send_message(cid, "사용하실 서비스를 선택하세요.", reply_markup=serviceSelect)
        #command_help(m)  # show the new user the help page
    else:
        bot.send_message(cid, "다시 오신 것을 환영합니다.")
        bot.send_message(cid, "사용하실 서비스를 선택하세요.", reply_markup=serviceSelect)

@bot.message_handler(commands=['Jobjang'])
def command_jobjang(m):
    cid = m.chat.id
    bot.send_message(cid, "당신이 관심있는 분야를 선택하세요.", reply_markup=articleSelectInline)  # show the keyboard
    userStep[cid] = 100  # set the user to the next step (expecting a reply in the listener now)

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
        bot.send_message(cid, "http://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=105&oid=421&aid=0002058351")



# chat_action example (not a good one...)
@bot.message_handler(commands=['sendLongText'])
def command_long_text(m):
    cid = m.chat.id
    bot.send_message(cid, "If you think so...")
    bot.send_chat_action(cid, 'typing')  # show the bot "typing" (max. 5 secs)
    time.sleep(3)
    bot.send_message(cid, ".")


# user can chose an image (multi-stage command example)
@bot.message_handler(commands=['getImage'])
def command_image(m):
    cid = m.chat.id
    bot.send_message(cid, "이미지를 선택하세요.", reply_markup=imageSelect)  # show the keyboard
    userStep[cid] = 1  # set the user to the next step (expecting a reply in the listener now)

# 기사 가져오기
@bot.message_handler(commands=['getArticle'])
def command_article(m):
    cid = m.chat.id
    bot.send_message(cid, "당신이 관심있는 분야를 선택하세요.", reply_markup=articleSelectInline)  # show the keyboard
    userStep[cid] = 100  # set the user to the next step (expecting a reply in the listener now)


# if the user has issued the "/getImage" command, process the answer
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 1)
def msg_image_select(m):
    cid = m.chat.id
    text = m.text

    # for some reason the 'upload_photo' status isn't quite working (doesn't show at all)
    bot.send_chat_action(cid, 'typing')

    if text == "닭":  # send the appropriate image based on the reply to the "/getImage" command
        bot.send_photo(cid, open('rooster.jpg', 'rb'),
                       reply_markup=hideBoard)  # send file and hide keyboard, after image is sent
        userStep[cid] = 0  # reset the users step back to 0
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

# if the user has issued the "/getImage" command, process the answer
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 100)
def msg_article_select(m):
    cid = m.chat.id
    text = m.text

    # for some reason the 'upload_photo' status isn't quite working (doesn't show at all)
    bot.send_chat_action(cid, 'typing')

    if text == "IT":  # send the appropriate image based on the reply to the "/getImage" command
        bot.send_message(cid, "IT Article!!")
        userStep[cid] = 0  # reset the users step back to 0
    elif text == "사회":
        bot.send_message(cid, "사회 기사!!")
        userStep[cid] = 0
    else:
        bot.send_message(cid, "잘못 입력하였습니다.")
        userStep[cid] = 0


# filter on a specific message
@bot.message_handler(func=lambda message: message.text == "hi")
def command_text_hi(m):
    bot.send_message(m.chat.id, "안녕!")


# default handler for every other text
@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    # this is the standard reply to a normal message
    text = m.text
    if text == "Jobjang":
        command_jobjang(m)
    else:
        bot.send_message(m.chat.id, "무슨 말인지 모르겠습니다. \"" + m.text + "\"\n여기서 사용가능한 명령어를 확인하세요! /help")

# 여기서 부터 callback_query 핸들러
"""====================================================SET======================================================"""
@bot.callback_query_handler(func=lambda call: call.data == "100-1" and get_user_step(call.from_user.id) == 100)
def step100IT(call):
    cid = call.from_user.id
    #bot.answer_callback_query(call.id, text="IT 기사!!")
    bot.send_message(cid, "어떤 종류의 IT 글을 원하시나요?", reply_markup=step110Keyboard)
    userStep[cid] = 110

@bot.callback_query_handler(func=lambda call: call.data == "100-2" and get_user_step(call.from_user.id) == 100)
def step100Social(call):
    cid = call.from_user.id
    #bot.answer_callback_query(call.id, text="사회 기사!!")
    bot.send_message(cid, "어떤 종류의 사회 글을 원하시나요?", reply_markup=step120Keyboard)
    userStep[cid] = 120
"""============================================================================================================="""

"""====================================================SET======================================================"""
@bot.callback_query_handler(func=lambda call: call.data == "110-1" and get_user_step(call.from_user.id) == 110)
def step100Social(call):
    cid = call.from_user.id
    #bot.answer_callback_query(call.id, text="사회 기사!!")
    bot.send_message(cid, "IT 기사 목록입니다.")
    userStep[cid] = 0

@bot.callback_query_handler(func=lambda call: call.data == "110-2" and get_user_step(call.from_user.id) == 110)
def step100Social(call):
    cid = call.from_user.id
    #bot.answer_callback_query(call.id, text="사회 기사!!")
    bot.send_message(cid, "IT 구인 정보 목록입니다.")
    userStep[cid] = 0
"""============================================================================================================="""

"""====================================================SET======================================================"""
@bot.callback_query_handler(func=lambda call: call.data == "120-1" and get_user_step(call.from_user.id) == 120)
def step100Social(call):
    cid = call.from_user.id
    #bot.answer_callback_query(call.id, text="사회 기사!!")
    bot.send_message(cid, "사회 기사 목록입니다.")
    userStep[cid] = 0

@bot.callback_query_handler(func=lambda call: call.data == "120-2" and get_user_step(call.from_user.id) == 120)
def step100Social(call):
    cid = call.from_user.id
    #bot.answer_callback_query(call.id, text="사회 기사!!")
    bot.send_message(cid, "사회 구인 정보 목록입니다.")
    userStep[cid] = 0
"""============================================================================================================="""

bot.polling()
