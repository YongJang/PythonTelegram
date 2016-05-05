# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.
import pymysql
import sys
import telebot

API_TOKEN = '207944330:AAGdpOvswmHangYooE8wBEf1p-vYP2skyL0'

bot = telebot.TeleBot(API_TOKEN)

# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, "Wellcome!! This is an article bot!")


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)

bot.polling()
