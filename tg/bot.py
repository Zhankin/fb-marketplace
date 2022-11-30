import os
import telepot

bot = telepot.Bot(os.environ['TOKEN'])
CHAT_ID = os.environ['CHAT_ID']


def send_message_tg(text):
    bot.sendMessage(CHAT_ID, text)


def send_tg(text, image_url):
    bot.sendPhoto(CHAT_ID, image_url, caption=text)
