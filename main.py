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


import requests

url = "https://open-weather13.p.rapidapi.com/city/fivedaysforcast/55.7522/37.6156"

headers = {
	"X-RapidAPI-Key": "c631a4d29emshb66eb14026d7ad6p17b874jsn8f480c04f855",
	"X-RapidAPI-Host": "open-weather13.p.rapidapi.com"
}

response = requests.get(url, headers=headers)

print(response.json())

#обычный {'coord': {'lon': 37.6156, 'lat': 55.7522}, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04d'}], 'base': 'stations', 'main': {'temp': 43.18, 'feels_like': 41.68, 'temp_min': 41.56, 'temp_max': 44.46, 'pressure': 1002, 'humidity': 79, 'sea_level': 1002, 'grnd_level': 984}, 'visibility': 10000, 'wind': {'speed': 3.27, 'deg': 264, 'gust': 4.79}, 'clouds': {'all': 100}, 'dt': 1697464428, 'sys': {'type': 2, 'id': 2000314, 'country': 'RU', 'sunrise': 1697428864, 'sunset': 1697466541}, 'timezone': 10800, 'id': 524901, 'name': 'Moscow', 'cod': 200}