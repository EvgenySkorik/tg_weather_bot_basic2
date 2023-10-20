# import telebot
# from settings import SiteSettings
#
# from database.common.models import db, History
# from database.core import crud
# from SITE_API.core import headers, site_api, url
#
# tg_bot = SiteSettings()
# bot = telebot.TeleBot(tg_bot.tg_api)
#
# db_write = crud.create()
# db_read = crud.retrieve()
#
#
# @bot.message_handler(commands=['start', 'help'])
# def start(message):
#     print(message.text)
#
#     if message.text == '/start':
#         weather = site_api.get_response()
#         response = weather(url, 'moscow', headers)
#         bot.send_message(message.chat.id, f'Приветствуем {message.from_user.username} это БОТ по определению погоды!\n'
#                                           f'Для информации по командам наберите /help\n'
#                                           f'Или воспользуйтесь кнопками ниже')
#         data = [{'temp_now': response[0], 'temp_like_now': response[1]}]
#         print(data)
#         bot.send_message(message.chat.id, f'Температура в москве {response[0]} градуса по цельсию.,\n'
#                                           f'Ощущается как {response[1]}')
#     elif message.text == '/help':
#         bot.send_message(message.chat.id, '/start - запуск бота или возврат в основное меню\n'
#                                           '/help - доступные команды\n'
#                                           '/low - \n'
#                                           '/hight - \n'
#                                           '/custom - 2345')
#
#
#
# bot.polling(none_stop=True)
import peewee
#
# import requests
#
# url = "https://open-weather13.p.rapidapi.com/city/певек"
#
# headers = {
# 	"X-RapidAPI-Key": "c631a4d29emshb66eb14026d7ad6p17b874jsn8f480c04f855",
# 	"X-RapidAPI-Host": "open-weather13.p.rapidapi.com"
# }
#
# response = requests.get(url, headers=headers)



from peewee import *
# from database.common.models import History
#
# db = peewee.SqliteDatabase('C:\Python\python_basic_diploma\TG_API\loging_base.db')
# db.connect()
#
# print(db.get_context_options())
# for i in History.select():
#     print(i.user_name)


# for i in db.select():
#     print(i)


# a = History.get(History.user_name=='Evgeny_SK')
# print(a)