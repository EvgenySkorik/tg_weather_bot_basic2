import telebot
from settings import SiteSettings
from datetime import datetime

from database.common.models import db, History
from database.core import crud
from SITE_API.core import headers, site_api, url

tg_bot = SiteSettings()
bot = telebot.TeleBot(tg_bot.tg_api)

db_write = crud.create()
db_read = crud.retrieve()



@bot.message_handler(commands=['start'])
def start(message):
    answer = 'Добрый день' if 6 < datetime.now().hour < 17 else 'Добрый вечер'
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    bt1 = telebot.types.KeyboardButton('Узнать погоду в городе')
    bt2 = telebot.types.KeyboardButton('Информация по командам')
    markup.add(bt1, bt2)
    bot.send_message(message.chat.id, f'{answer} <b>{message.from_user.username}</b> это ТелеграмБот по определению погоды!',
                     reply_markup=markup, parse_mode='html')


def info(message):
    bot.send_message(message.chat.id, '<b>Список доступных команд:</b>', parse_mode='html')
    bot.send_message(message.chat.id, '2. /start - запуск бота или возврат в основное меню')
    bot.send_message(message.chat.id, '3. /low')
    bot.send_message(message.chat.id, '4. /hight')
    bot.send_message(message.chat.id, '4. /custom - 2345')

def get_weather(message):
    db_write = crud.create()
    db_read = crud.retrieve()

    weather = site_api.get_response()
    response = weather(url, message.text, headers)
    data = [{'user_name': message.from_user.username, 'temp_now': response[0], 'temp_like_now': response[1]}]
    db_write(db, History, data)

    bot.send_message(message.chat.id, f'Погода в {message.text} - {response[0]} по цельсию\n'
                                      f'Ощущается как - {response[1]} по цельсию')

@bot.message_handler(content_types=['text'])
def menu(message):
    if message.text.lower() == 'узнать погоду в городе':
        bot.send_message(message.chat.id, 'Напишите в чат бота название города на англиском или русском языке')
        bot.register_next_step_handler(message, get_weather)
    elif message.text.lower() == 'информация по командам':
        info(message)




if __name__ == '__main__':
    bot.polling(none_stop=True)