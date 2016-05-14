

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
import requests
import re

API_TOKEN = '207944330:AAGdpOvswmHangYooE8wBEf1p-vYP2skyL0'

BASE_URL = 'https://api.telegram.org/bot' + API_TOKEN + '/'
bot = telebot.TeleBot(API_TOKEN)

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
    else:
        bot.reply_to(message, message.text)



bot.polling()
