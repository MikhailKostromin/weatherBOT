import telebot
from telebot import types
import config
import requests, json
from datetime import datetime


# Функция парcинга сайта и отправки цены биткойн пользователю
# def get_data():
#     req = requests.get('https://yobit.net/api/3/ticker/btc_usd')
#     response = req.json()
#     sell_price = response['btc_usd']['sell']
#     return f"{datetime.now().strftime('%Y-%m-%d %H:%M')}\nСтоимость BTC: {sell_price}$"


def weather(city, API_KEY):
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
    URL = BASE_URL + "q=" + city + "&appid=" + API_KEY
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        temperature = int(data['main']['temp'] - 273.15)
        return temperature
    else:
        print("Error in HTTP request")


bot = telebot.TeleBot(config.TELEGRAM_API_KEY)


@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    weather_btn = types.KeyboardButton('Погода')
    markup.add(weather_btn)
    msg = bot.reply_to(message, "Здравствуйте! Я - бот показывающий текущую погоду \U0001F31E по городу.")
    bot.send_message(message.chat.id, f"{message.from_user.first_name}, введите название города, чтобы продолжить",
                     reply_markup=markup)
    bot.register_next_step_handler(msg, print_weather)


def print_weather(message):
    city = message.text
    temperature = weather(city, config.WEATHER_API_KEY)
    msg = bot.reply_to(message, f"Текущая температура: {temperature}°C")
    bot.send_message(message.chat.id, "Введите название города, чтобы продолжить")
    bot.register_next_step_handler(msg, print_weather)


# def send_text(message):
#     if message.chat.type == 'private':
#         if message.text == '💰 Цена Bitcoin':
#             bot.send_message(message.chat.id, get_data())

bot.polling()
