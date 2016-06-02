import telebot

TOKEN = '207944330:AAGdpOvswmHangYooE8wBEf1p-vYP2skyL0'
CHAT_ID = '202899924'

bot = telebot.TeleBot(TOKEN)

ret_msg = bot.send_voice(CHAT_ID, open('tests/test_data/record.ogg'))

file_info = bot.get_file(ret_msg.voice.file_id)

downloaded_file = bot.download_file(file_info.file_path)

with open('new_file.ogg', 'wb') as new_file:
    new_file.write(downloaded_file)
