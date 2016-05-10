

# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.
# INLINE KEYBOARD REFERENCED FROM https://github.com/yagop/node-telegram-bot-api/issues/109 -- yongjang
# https://github.com/eternnoir/pyTelegramBotAPI/blob/bot20/examples/bot20-pass_generator-example.py


import pymysql
import sys
import telebot
from telebot import types
import urllib
import urllib.parse
import json
import logging
import re

API_TOKEN = '207944330:AAGdpOvswmHangYooE8wBEf1p-vYP2skyL0'

BASE_URL = 'https://api.telegram.org/bot' + API_TOKEN + '/'
bot = telebot.TeleBot(API_TOKEN)

markup = types.ReplyKeyboardMarkup()
itembtn1 = types.KeyboardButton('1')
itembtn2 = types.KeyboardButton('2')
itembtn3 = types.KeyboardButton('3')
itembtn4 = types.KeyboardButton('4')
markup.row(itembtn1,itembtn2)
markup.row(itembtn3,itembtn4)

hideBoard = types.ReplyKeyboardHide()


# 봇이 응답할 명령어
CMD_START     = '/start'
CMD_STOP      = '/stop'
CMD_HELP      = '/help'
CMD_USER      = '/user'
CMD_BROADCAST = '/broadcast'

# 커스텀 키보드
CUSTOM_KEYBOARD = [
        [CMD_START],
        [CMD_STOP],
        [CMD_HELP],
        [CMD_USER],
        ]

# 메시지 발송 관련 함수들
def send_msg(chat_id, text, reply_to=None, no_preview=True, keyboard=None):
    u"""send_msg: 메시지 발송
    chat_id:    (integer) 메시지를 보낼 채팅 ID
    text:       (string)  메시지 내용
    reply_to:   (integer) ~메시지에 대한 답장
    no_preview: (boolean) URL 자동 링크(미리보기) 끄기
    keyboard:   (list)    커스텀 키보드 지정
    """
    params = {
        'chat_id': str(chat_id),
        'text': text.encode('utf-8'),
        }
    if reply_to:
        params['reply_to_message_id'] = reply_to
    if no_preview:
        params['disable_web_page_preview'] = no_preview
    if keyboard:
        reply_markup = json.dumps({
            'keyboard': keyboard,
            'resize_keyboard': True,
            'one_time_keyboard': False,
            'selective': (reply_to != None),
            })
        params['reply_markup'] = reply_markup
    try:
        urllib2.urlopen(BASE_URL + 'sendMessage', urllib.urlencode(params)).read()
    except Exception as e:
        logging.exception(e)



# Handle '/start' and '/help'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    bot.reply_to(message, "Wellcome!! This is an article bot!")

@bot.message_handler(commands=['help'])
def help_message(message):
    bot.reply_to(message, "This is a help message!")

@bot.message_handler(commands=['user'])
def user_message(message):
    bot.reply_to(message, "Hi " + message.from_user.first_name + "!!")



# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    chat_id = message.chat.id
    if message.text == "Hello" or message.text ==  "Hi" or message.text ==  "안녕" or message.text ==  "안녕하세요" :
        bot.reply_to(message, "Hello " + message.from_user.first_name + "!!")
        #bot.send_message(chat_id, "button", keyboard = CUSTOM_KEYBOARD)
        send_msg(chat_id, "abc123", keyboard=CUSTOM_KEYBOARD)
    else:
        bot.reply_to(message, message.text)
        process_cmds(message)


u"""
=============================================================================================================
"""

# 봇 명령 처리 함수들
def cmd_start(chat_id):
    u"""cmd_start: 봇을 활성화하고, 활성화 메시지 발송
    chat_id: (integer) 채팅 ID
    """
    send_msg(chat_id, MSG_START, keyboard=CUSTOM_KEYBOARD)

def cmd_stop(chat_id):
    u"""cmd_stop: 봇을 비활성화하고, 비활성화 메시지 발송
    chat_id: (integer) 채팅 ID
    """
    send_msg(chat_id, MSG_STOP)

def cmd_help(chat_id):
    u"""cmd_help: 봇 사용법 메시지 발송
    chat_id: (integer) 채팅 ID
    """
    send_msg(chat_id, USAGE, keyboard=CUSTOM_KEYBOARD)

def cmd_broadcast(chat_id, text):
    u"""cmd_broadcast: 봇이 활성화된 모든 채팅에 메시지 방송
    chat_id: (integer) 채팅 ID
    text:    (string)  방송할 메시지
    """
    send_msg(chat_id, u'메시지를 방송합니다.', keyboard=CUSTOM_KEYBOARD)
    broadcast(text)

def cmd_echo(chat_id, text, reply_to):
    u"""cmd_echo: 사용자의 메시지를 따라서 답장
    chat_id:  (integer) 채팅 ID
    text:     (string)  사용자가 보낸 메시지 내용
    reply_to: (integer) 답장할 메시지 ID
    """
    send_msg(chat_id, text, reply_to=reply_to)

def process_cmds(msg):
    u"""사용자 메시지를 분석해 봇 명령을 처리
    chat_id: (integer) 채팅 ID
    text:    (string)  사용자가 보낸 메시지 내용
    """
    msg_id = msg.gessage_id
    chat_id = msg.chat.id
    text = msg.get('text')
    if (not text):
        return
    if CMD_START == text:
        cmd_start(chat_id)
        return
        u"""
    if (not get_enabled(chat_id)):
        return
        """
    if CMD_STOP == text:
        cmd_stop(chat_id)
        return
    if CMD_HELP == text:
        cmd_help(chat_id)
        return
    cmd_broadcast_match = re.match('^' + CMD_BROADCAST + ' (.*)', text)
    if cmd_broadcast_match:
        cmd_broadcast(chat_id, cmd_broadcast_match.group(1))
        return
    cmd_echo(chat_id, text, reply_to=msg_id)
    return



u"""
========================================================================================================================
"""


@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 1)
def msg_button_select(m):
    cid = m.chat.id
    text = m.text

    # for some reason the 'upload_photo' status isn't quite working (doesn't show at all)
    bot.send_chat_action(cid, 'typing')

    if text == "1":  # send the appropriate image based on the reply to the "/getImage" command
        bot.send_message(cid, "1", reply_markup = hideBoard)
    elif text == "2":
        bot.send_message(cid, "2", reply_markup = hideBoard)
    elif text == "3":
        bot.send_message(cid, "3", reply_markup = hideBoard)
    elif text == "4":
        bot.send_message(cid, "4", reply_markup = hideBoard)
    else :
        bot.send_message(cid, "Don't type bullsh*t, if I give you a predefined keyboard!")
        bot.send_message(cid, "Please try again")

u"""
# 웹 요청에 대한 핸들러 정의
# /me 요청시
class MeHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(json.dumps(json.load(urllib.parse.request(BASE_URL + 'getMe'))))

# /updates 요청시
class GetUpdatesHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(json.dumps(json.load(urllib.parse.request(BASE_URL + 'getUpdates'))))

# /set-wehook 요청시
class SetWebhookHandler(webapp2.RequestHandler):
    def get(self):
        url = self.request.get('url')
        if url:
            self.response.write(json.dumps(json.load(urllib.parse.request(BASE_URL + 'setWebhook', urllib.urlencode({'url': url})))))

# /webhook 요청시 (텔레그램 봇 API)
class WebhookHandler(webapp2.RequestHandler):
    def post(self):
        body = json.loads(self.request.body)
        self.response.write(json.dumps(body))
        process_cmds(body['message'])

"""

bot.polling()
