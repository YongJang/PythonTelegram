# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.
# INLINE KEYBOARD REFERENCED FROM https://github.com/yagop/node-telegram-bot-api/issues/109 -- yongjang

import pymysql
import sys
import telebot

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
    bot.reply_to(message, "Hello " + message.from_user.first_name + "!!")

# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    if message.text in "Hello" or "Hi" or "안녕" or "안녕하세요" :
        bot.reply_to(message, "Hello " + message.from_user.first_name + "!!")
    else:
        bot.reply_to(message, message.text)

bot.polling()
