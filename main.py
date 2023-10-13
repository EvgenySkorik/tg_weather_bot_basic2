import telebot
from settings import SiteSettings

from database.common.models import db, History
from database.core import crud
from SITE_API.core import headers, site_api, url

tg_bot = SiteSettings()
bot = telebot.TeleBot(tg_bot.tg_api)

db_write = crud.create()
db_read = crud.retrieve()


@bot.message_handler(commands=['start', 'help'])
def start(message):
    print(message.text)

    if message.text == '/start':
        weather = site_api.get_response()
        response = weather(url, 'moscow', headers)
        bot.send_message(message.chat.id, f'Приветствуем {message.from_user.username} это БОТ по определению погоды!\n'
                                          f'Для информации по командам наберите /help\n'
                                          f'Или воспользуйтесь кнопками ниже')
        data = [{'temp_now': response[0], 'temp_like_now': response[1]}]
        print(data)
        bot.send_message(message.chat.id, f'Температура в москве {response[0]} градуса по цельсию.,\n'
                                          f'Ощущается как {response[1]}')
    elif message.text == '/help':
        bot.send_message(message.chat.id, '/start - запуск бота или возврат в основное меню\n'
                                          '/help - доступные команды\n'
                                          '/low - \n'
                                          '/hight - \n'
                                          '/custom - 2345')



bot.polling(none_stop=True)