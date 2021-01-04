import json
import os

import requests
import telebot
from flask import Flask, request
from telebot.types import InlineKeyboardButton

TOKEN = '1565130854:AAECOdx2Xg-SAPqHgbahTlRthh2_waHnB1s'
bot = telebot.TeleBot(TOKEN)

markup = telebot.types.ReplyKeyboardMarkup()
markup.row_width = 2
markup.add(
    InlineKeyboardButton('BTC/USD', callback_data='btc/usd'),
    InlineKeyboardButton('BTC/RUB', callback_data='btc/rub')
)

server = Flask(__name__)


def get_btc_price(currency: str):
    resp = requests.get(
        f'https://blockchain.info/ticker'
    )
    return json.loads(resp.text).get(currency.upper()).get('last')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет! Ожидаю команду.',
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def send_currency(message):
    answer = 'Wrong input :('
    if message.text.lower() == 'btc/usd':
        answer = get_btc_price('usd')
    if message.text.lower() == 'btc/rub':
        answer = get_btc_price('rub')
    bot.send_message(message.chat.id, answer)


@server.route('/' + TOKEN, methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://denvy-telebot.herokuapp.com/' + TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
