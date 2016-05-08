# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.
# INLINE KEYBOARD REFERENCED FROM https://github.com/yagop/node-telegram-bot-api/issues/109 -- yongjang

import pymysql
import sys
import telebot
from telebot import types

API_TOKEN = '207944330:AAGdpOvswmHangYooE8wBEf1p-vYP2skyL0'

bot = telebot.TeleBot(API_TOKEN)

# Handle '/start' and '/help'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Wellcome!! This is an article bot!")

@bot.message_handler(commands=['help'])
def help_message(message):
    bot.reply_to(message, "This is a help message!")

@bot.message_handler(commands=['user'])
def user_message(message):
    bot.reply_to(message, "Hi " + message.from_user.first_name + "!!")

markup = types.ReplyKeyboardMarkup()
itembtn1 = types.KeyboardButton('1')
itembtn2 = types.KeyboardButton('2')
itembtn3 = types.KeyboardButton('3')
itembtn4 = types.KeyboardButton('4')
markup.row(itembtn1,itembtn2)
markup.row(itembtn3,itembtn4)

# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    if message.text == "Hello" or message.text ==  "Hi" or message.text ==  "안녕" or message.text ==  "안녕하세요" :
        bot.reply_to(message, "Hello " + message.from_user.first_name + "!!")
        bot.send_message(chai_id, "button", reply_markup = markup)
    else:
        bot.reply_to(message, message.text)

bot.polling()
