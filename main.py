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

url = "https://open-weather13.p.rapidapi.com/city/певек"

headers = {
	"X-RapidAPI-Key": "c631a4d29emshb66eb14026d7ad6p17b874jsn8f480c04f855",
	"X-RapidAPI-Host": "open-weather13.p.rapidapi.com"
}

response = requests.get(url, headers=headers)

import pprint

# data = {'coord': {'lon': 37.6156, 'lat': 55.7522}, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10n'}], 'base': 'stations', 'main': {'temp': 39.49, 'feels_like': 31.39, 'temp_min': 38.55, 'temp_max': 40.01, 'pressure': 1005, 'humidity': 92, 'sea_level': 1005, 'grnd_level': 987}, 'visibility': 3611, 'wind': {'speed': 14.34, 'deg': 276, 'gust': 26.33}, 'rain': {'1h': 0.22}, 'clouds': {'all': 100}, 'dt': 1697567601, 'sys': {'type': 2, 'id': 2000314, 'country': 'RU', 'sunrise': 1697515386, 'sunset': 1697552793}, 'timezone': 10800, 'id': 524901, 'name': 'Moscow', 'cod': 200}
# pprint.pprint(data)
data = response.json()
res = data.get('weather', None)[0].get('main', None)

print(res)
if 'Rain' in res:
    print('Дождик')


#Rain - дождь, Clouds - облачно, Clear - ясно,

