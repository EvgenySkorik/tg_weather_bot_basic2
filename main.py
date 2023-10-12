import abc
import requests
import telebot
import json
from settings import SiteSettings
tg = SiteSettings()

bot = telebot.TeleBot('6351189777:AAFlSX8Yfd-6RSQD1SVhM1cRKiHfTFrvdC0')
# bot = telebot.TeleBot(tg.tg_api)

# API = '8a9ffc6457mshc1d2ca862369e02p15737cjsn490c2f4bc410'
URL = 'https://open-weather13.p.rapidapi.com/city/'
headers = {
    "X-RapidAPI-Key": "8a9ffc6457mshc1d2ca862369e02p15737cjsn490c2f4bc410",
    "X-RapidAPI-Host": "open-weather13.p.rapidapi.com"
}


def far_to_cel(num: float) -> float:
    return round((num - 32) / 1.8, 2)


@bot.message_handler(commands=['start', 'help'])
def start(message):
    print(message.text)

    if message.text == '/start':
        res = requests.get(URL + 'moscow', headers=headers)
        bot.send_message(message.chat.id, f'Приветствуем {message.from_user.username} это БОТ по определению погоды!\n'
                                          f'Для информации по командам наберите /help\n'
                                          f'Или воспользуйтесь кнопками ниже')
        data = json.loads(res.text)
        print(data)
        bot.send_message(message.chat.id, f'Температура в москве {far_to_cel(data["main"]["temp"])} градуса по цельсию.')
    elif message.text == '/help':
        bot.send_message(message.chat.id, '/start - запуск бота или возврат в основное меню\n'
                                          '/help - доступные команды\n'
                                          '/low - \n'
                                          '/hight - \n'
                                          '/custom - 2345')



bot.polling(none_stop=True)
