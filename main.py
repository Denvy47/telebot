import json

import requests
import telebot

bot = telebot.TeleBot('1565130854:AAECOdx2Xg-SAPqHgbahTlRthh2_waHnB1s')

keyboard = telebot.types.ReplyKeyboardMarkup()
keyboard.row('BTC/USD', 'BTC/RUB')


def get_btc_price(currency: str):
    resp = requests.get(
        f'https://blockchain.info/ticker'
    )
    return json.loads(resp.text).get(currency.upper()).get('last')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет! Ожидаю команду.',
                     reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def send_currency(message):
    answer = 'Wrong input :('
    if message.text.upper() == 'BTC/USD':
        answer = get_btc_price('usd')
    if message.text.upper() == 'BTC/RUB':
        answer = get_btc_price('rub')
    bot.send_message(message.chat.id, answer)


bot.polling()
