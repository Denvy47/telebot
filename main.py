import json

import requests
import telebot
from telebot.types import InlineKeyboardButton

_USD = 'BTC/USD'
_RUB = 'BTC/RUB'

bot = telebot.TeleBot('1565130854:AAECOdx2Xg-SAPqHgbahTlRthh2_waHnB1s')

markup = telebot.types.ReplyKeyboardMarkup()
markup.row_width = 2
markup.add(
    InlineKeyboardButton(_USD),
    InlineKeyboardButton(_RUB)
)

bot.delete_webhook()


def get_btc_price(currency: str):
    resp = requests.get('https://blockchain.info/ticker')
    return json.loads(resp.text).get(currency).get('last')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет! Ожидаю команду.',
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def send_price(message):
    answer = 'Неверная команда..Попробуй еще разок!'
    msg = message.text.upper()
    if msg in [_USD, _RUB]:
        answer = get_btc_price(msg.split('/')[1])
    bot.send_message(message.chat.id, answer)


bot.polling(none_stop=True, interval=0)
