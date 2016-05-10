# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.
# INLINE KEYBOARD REFERENCED FROM https://github.com/yagop/node-telegram-bot-api/issues/109 -- yongjang
# https://github.com/eternnoir/pyTelegramBotAPI/blob/bot20/examples/bot20-pass_generator-example.py

﻿#-*- encoding: utf-8 -*-

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

reply_markup = json.dumps({
    'keyboard': keyboard,
    'resize_keyboard': True,
    'one_time_keyboard': False,
    'selective': (reply_to != None),
    })

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
        bot.send_message(chat_id, "button", keyboard = CUSTOM_KEYBOARD)
    else:
        bot.reply_to(message, message.text)


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

bot.polling()
