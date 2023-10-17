import telebot
from settings import SiteSettings
from datetime import datetime

from database.common.models import db, History, ModelBase
from database.core import crud
from SITE_API.core import headers, site_api, url

tg_bot = SiteSettings()
bot = telebot.TeleBot(tg_bot.tg_api)

db_write = crud.create()
db_read = crud.retrieve()


ex1_type_err = 'Что-то не так!\n<b>Возможно, Вы ввели команду, вместо города или не существующий город!</b>\nВведите команду: /start '

@bot.message_handler(commands=['start', 'low', 'hight', 'custom', 'history'])
def start(message):
    print(message.text)
    if message.text == '/start':
        answer = 'Добрый день' if 6 < datetime.now().hour < 17 else 'Добрый вечер'
        markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        bt1 = telebot.types.KeyboardButton('Узнать погоду в городе')
        bt2 = telebot.types.KeyboardButton('Информация по командам')
        markup.add(bt1, bt2)
        bot.send_message(message.chat.id,
                         f'{answer} <b>{message.from_user.username}</b> это ТелеграмБот по определению погоды!',
                         reply_markup=markup, parse_mode='html')
    elif message.text == '/low':
        print(message.text)
        bot.send_message(message.chat.id, 'Напишите в каком городе хотите узнать минимальную температуру за сегодня:')
        bot.register_next_step_handler(message, get_weather_min)
    elif message.text == '/hight':
        bot.send_message(message.chat.id, 'Напишите в каком городе хотите узнать максимальную температуру за сегодня:')
        bot.register_next_step_handler(message, get_weather_max)
    elif message.text == '/history':
        print(message.text)
        bot.send_message(message.chat.id, '<b>Список запросов пользователя:</b>', parse_mode='html')
        history(message)


def info(message):
    bot.send_message(message.chat.id, '<b>Список доступных команд:</b>\nВведите команду в чат месенджера', parse_mode='html')
    bot.send_message(message.chat.id, '1. /start - запуск бота или возврат в основное меню')
    bot.send_message(message.chat.id, '2. /low - узнать минимальную температура за сегодня')
    bot.send_message(message.chat.id, '3. /hight - узнать максимальную температура за сегодня')
    bot.send_message(message.chat.id, '4. /custom - 2345')
    bot.send_message(message.chat.id, '5. /history - Истоия запросов.')


def get_weather(message):
    try:
        db_write = crud.create()

        weather = site_api.get_response()
        response = weather(url, message.text, headers)
        data = [{'user_name': message.from_user.username, 'user_city': message.text, 'temp_now': response[0], 'temp_like_now': response[1], 'other': 0}]
        db_write(db, History, data)

        bot.send_message(message.chat.id, f'Погода в {message.text}: <b>{response[0]}</b> по цельсию\n'
                                          f'Ощущается как: <b>{response[1]}</b> по цельсию', parse_mode='html')
    except TypeError:
        bot.send_message(message.chat.id, ex1_type_err, parse_mode='html')

def get_weather_min(message):
    try:
        db_write = crud.create()

        weather = site_api.get_response()
        response = weather(url, message.text, headers)
        data = [{'user_name': message.from_user.username, 'user_city': message.text, 'temp_now': 0, 'temp_like_now': 0, 'other': response[2]}]
        db_write(db, History, data)

        bot.send_message(message.chat.id, f'Минимальная температура за сегодня в {message.text}: <b>{response[2]}</b> '
                                          f'по цельсию', parse_mode='html')
    except TypeError:
        bot.send_message(message.chat.id, ex1_type_err, parse_mode='html')

def get_weather_max(message):
    try:
        db_write = crud.create()

        weather = site_api.get_response()
        response = weather(url, message.text, headers)
        data = [{'user_name': message.from_user.username, 'user_city': message.text, 'temp_now': 0, 'temp_like_now': 0, 'other': response[3]}]
        db_write(db, History, data)

        bot.send_message(message.chat.id, f'Максимальнаяя температура за сегодня в {message.text}: <b>{response[3]}</b> '
                                          f'по цельсию', parse_mode='html')
    except TypeError:
        bot.send_message(message.chat.id, ex1_type_err, parse_mode='html')

def history(message):
    db_read = crud.retrieve()

    retrieved = db_read(db, History, History.user_name, History.user_city, History.temp_now, History.temp_like_now, History.other)

    for el in retrieved:
        bot.send_message(message.chat.id, f'{el.user_name, el.user_city, el.temp_now, el.temp_like_now, el.other}')



@bot.message_handler(content_types=['text'])
def menu(message):
    if message.text.lower() == 'узнать погоду в городе':
        bot.send_message(message.chat.id, 'Напишите в чат бота название города на англиском или русском языке')
        bot.register_next_step_handler(message, get_weather)
    elif message.text.lower() == 'информация по командам':
        info(message)


# @bot.message_handler(commands=['low', 'hight', 'custom'])
# def user_commands(message):
#     if message.text == '/low':
#         print(message.text)
#         bot.send_message(message.chat.id, 'ЛОУ')
#     elif message.text == 'hight':
#         bot.send_message(message.chat.id, 'hight')


if __name__ == '__main__':
    bot.polling(none_stop=True)
