import json
import os

import requests
import telebot
from flask import Flask, request
from telebot.types import InlineKeyboardButton

_TOKEN = os.environ.get('TOKEN')
_USD = 'usd'
_RUB = 'rub'

bot = telebot.TeleBot(_TOKEN)

markup = telebot.types.ReplyKeyboardMarkup()
markup.row_width = 2
markup.add(
    InlineKeyboardButton('BTC/USD', callback_data=_USD),
    InlineKeyboardButton('BTC/RUB', callback_data=_RUB)
)

server = Flask(__name__)


def get_btc_price(currency: str):
    resp = requests.get('https://blockchain.info/ticker')
    return json.loads(resp.text).get(currency.upper()).get('last')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет! Ожидаю команду.',
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def send_currency(message):
    answer = 'Wrong input :('
    msg = message.text.lower()
    if msg in [_USD, _RUB]:
        answer = get_btc_price(msg)
    bot.send_message(message.chat.id, answer)


@server.route('/' + _TOKEN, methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://denvy-telebot.herokuapp.com/' + _TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
