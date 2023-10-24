import telebot
from settings import SiteSettings
from datetime import datetime
import os

from database.common.models import db, History
from database.core import crud
from site_api_weather.core import headers, site_api, url


tg_bot = SiteSettings()
bot = telebot.TeleBot(tg_bot.tg_api)

db_write = crud.create()
db_read = crud.retrieve()

ex1_type_err = 'Что-то не так!\n<b>Возможно, Вы ввели команду, вместо города или не существующий город!</b>\nВведите команду: /start '
iter_foto = iter([1, 2, 3])
iter_fact = iter([1, 2, 3])


def generic_path() -> None:
    '''Функция для генерации пути к папке Foto'''
    cur_path = os.path.dirname(__file__)
    new_path = os.path.join(cur_path, 'foto_pct')
    foto_list: list = [os.path.join(new_path, i_file) for i_file in os.listdir(new_path)]
    fact_list: list = ['Самая низкая температура в Москве за все время наблюдений – 17 июля 1940, было – 42,2 градуса',
                       'В Берлине дождь идет в среднем 100 дней в году. В городе 175 музеев. Так что каждый дождливый день вы можете посещать разные музеи',
                       'Самый холодный месяц в Москве – это февраль. Но, оказывается, что среднемесячная температура этого лютого месяца всего-то минус 6,7 градусов!',
                       'В английском языке есть более 100 слов для обозначения дождя',
                       'Минимальные месячные температуры в г. Казань наблюдались в январе 1891-го (-21 градус) и феврале 1954 года (-20 градусов)']
    global iter_foto
    iter_foto = iter(foto_list)
    global iter_fact
    iter_fact = iter(fact_list)


generic_path()


@bot.message_handler(commands=['start', 'low', 'high', 'custom', 'history'])
def start(message):
    """Функция - меню, выводит приветствие, создает кнопки и логику команд"""

    if message.text == '/start':
        answer = 'Добрый день' if 6 < datetime.now().hour < 17 else 'Добрый вечер'
        markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        bt1 = telebot.types.KeyboardButton('Узнать погоду в городе')
        bt2 = telebot.types.KeyboardButton('Информация по командам')
        bt3 = telebot.types.KeyboardButton('Погода в фотографиях')
        markup.add(bt1, bt2, bt3)
        bot.send_message(message.chat.id,
                         f'{answer} <b>{message.from_user.username}!</b> Вы можете воспользоваться кнопками '
                         f'ниже или использовать команды из меню\n', reply_markup=markup, parse_mode='html')
        bot.send_message(message.chat.id, '🌗')

    elif message.text == '/low':
        bot.send_message(message.chat.id, 'Напишите в каком городе хотите узнать минимальную температуру за сегодня:')
        bot.register_next_step_handler(message, get_weather_min)
    elif message.text == '/high':
        bot.send_message(message.chat.id, 'Напишите в каком городе хотите узнать максимальную температуру за сегодня:')
        bot.register_next_step_handler(message, get_weather_max)
    elif message.text == '/history':
        bot.send_message(message.chat.id, '<b>Ваши последние 10 запросов:</b>', parse_mode='html')
        history(message)
    else:
        bot.send_message(message.chat.id, 'Для того, чтобы повторить запрос воспользуйтесь кнопками или меню.')


def info(message):
    '''Функция - выводящая в чат месенджера список команд'''

    bot.send_message(message.chat.id, '<b>Список доступных команд:</b>\nВведите команду в чат месенджера',
                     parse_mode='html')
    bot.send_message(message.chat.id, '1. /start - запуск бота или возврат в основное меню')
    bot.send_message(message.chat.id, '2. /low - узнать минимальную температура за сегодня')
    bot.send_message(message.chat.id, '3. /high - узнать максимальную температура за сегодня')
    bot.send_message(message.chat.id, '4. /history - Истоия запросов.')


def emoji_determinant(responce: str) -> str:
    '''Функция принимает запрос по качеству погоды, возвращает эмодзи'''
    emoji = {'Rain': '🌨', 'Clouds': '⛅️', 'Clear': '☀️', 'Snow': '❄️'}
    if responce in emoji.keys():
        return emoji.get(responce)
    return '☀️'


def get_weather(message):
    """Функция делает запрос на API-сайт, выводит текущую температуру и температуру как ощущается, записывает запрос в БД"""
    try:
        weather = site_api.get_response()
        response = weather(url, message.text, headers)
        data = [{'user_name': message.from_user.username, 'user_city': message.text, 'temp_now': response[0],
                 'temp_like_now': response[1], 'other': 0}]
        db_write(db, History, data)

        bot.send_message(message.chat.id, f'Погода в {message.text}: <b>{response[0]}</b> ℃\n'
                                          f'Ощущается как: <b>{response[1]}</b> ℃ {emoji_determinant(response[4])}',
                         parse_mode='html')
    except TypeError:
        bot.send_message(message.chat.id, ex1_type_err, parse_mode='html')


def get_weather_min(message):
    """Функция делает запрос на API-сайт, выводит текущую минимальную температуру, записывает запрос в БД"""
    try:
        weather = site_api.get_response()
        response = weather(url, message.text, headers)
        data = [{'user_name': message.from_user.username, 'user_city': message.text, 'temp_now': 0, 'temp_like_now': 0,
                 'other': response[2]}]
        db_write(db, History, data)

        bot.send_message(message.chat.id, f'Минимальная температура за сегодня в {message.text}: <b>{response[2]}</b> '
                                          f'℃ {emoji_determinant(response[4])}', parse_mode='html')
    except TypeError:
        bot.send_message(message.chat.id, ex1_type_err, parse_mode='html')


def get_weather_max(message):
    """Функция делает запрос на API-сайт, выводит текущую максимальную температуру, записывает запрос в БД"""
    try:
        weather = site_api.get_response()
        response = weather(url, message.text, headers)
        data = [{'user_name': message.from_user.username, 'user_city': message.text, 'temp_now': 0, 'temp_like_now': 0,
                 'other': response[3]}]
        db_write(db, History, data)

        bot.send_message(message.chat.id,
                         f'Максимальнаяя температура за сегодня в {message.text}: <b>{response[3]}</b> ℃'
                         f'{emoji_determinant(response[4])}', parse_mode='html')
    except TypeError:
        bot.send_message(message.chat.id, ex1_type_err, parse_mode='html')


def history(message):
    """Функция выводит пользователю в чат мессенджера историю запросов"""
    db_read = crud.retrieve()

    retrieved = db_read(db, message.from_user.username, History, History.user_name, History.user_city, History.temp_now,
                        History.temp_like_now, History.other)

    for idx, el in enumerate(reversed(retrieved)):
        if idx == 10:
            break
        bot.send_message(message.chat.id, f'{el.user_name, el.user_city, el.temp_now, el.temp_like_now, el.other}')


def get_foto(message, path, fact):
    '''Функция открывает фото по пути, отправляет фото в месенджер'''
    with open(path, 'rb') as f:
        bot.send_message(message.chat.id, fact)
        bot.send_photo(message.chat.id, f)


@bot.message_handler(content_types=['text'])
def menu(message):
    '''Функция - обрабатывающая нажатие кнопок из меню'''

    if message.text.lower() == 'узнать погоду в городе':
        bot.send_message(message.chat.id, 'Напишите в чат бота название города на англиском или русском языке')
        bot.register_next_step_handler(message, get_weather)
    elif message.text.lower() == 'информация по командам':
        info(message)
    elif message.text.lower() == 'погода в фотографиях':
        try:
            get_foto(message, path=next(iter_foto), fact=next(iter_fact))
        except (TimeoutError, ConnectionError, ConnectionAbortedError, ConnectionAbortedError):
            get_foto(message, path=next(iter_foto), fact=next(iter_fact))
        except StopIteration:
            generic_path()
    else:
        bot.send_message(message.chat.id, f'{message.from_user.username}, вы ввели: {message.text}, \n<b>Воспользуйтесь '
                                          f'кнопками или используйте команды из меню</b>', parse_mode='html')


while True:
    try:
        if __name__ == '__main__':
            bot.polling(none_stop=True)
    except:
        continue
# if __name__ == '__main__':
#     bot.polling(none_stop=True)