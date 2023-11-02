import telebot
from settings import SiteSettings
import os
import random

from database.common.models import db, History
from database.core import crud
from site_api_weather.core import headers, site_api, url

tg_bot = SiteSettings()
bot = telebot.TeleBot(tg_bot.tg_api)

db_write = crud.create()
db_read = crud.retrieve()


def _info(message):
    '''Функция - выводящая в чат месенджера список команд'''

    bot.send_message(message.chat.id, '<b>Список доступных команд:</b>\nВведите команду в чат месенджера',
                     parse_mode='html')
    bot.send_message(message.chat.id, '1. /start - запуск бота или возврат в основное меню')
    bot.send_message(message.chat.id, '2. /low - узнать минимальную температура за сегодня')
    bot.send_message(message.chat.id, '3. /high - узнать максимальную температура за сегодня')
    bot.send_message(message.chat.id, '4. /history - Истоия запросов.')


def emoji_determinant(responce: str) -> str:
    '''Функция принимает запрос по качеству погоды, возвращает эмодзи'''
    emoji: dict = {'Rain': '🌨', 'Clouds': '⛅️', 'Clear': '☀️', 'Snow': '❄️'}
    if responce in emoji.keys():
        return emoji.get(responce)
    return '☀️'


ex1_type_err: str = 'Что-то не так!\n<b>Возможно, Вы ввели команду, вместо города или не существующий город!</b>' \
                    '\nВведите команду: /start '


def _get_weather(message):
    """Функция делает запрос на API-сайт, выводит текущую температуру и температуру как ощущается, записывает запрос в БД"""
    try:
        weather = site_api.get_response()
        response = weather(url, message.text, headers)
        data = [{'user_name': message.from_user.first_name, 'user_city': message.text, 'temp_now': response[0],
                 'temp_like_now': response[1], 'other': 0}]
        db_write(db, History, data)

        bot.send_message(message.chat.id, f'Погода в {message.text}: <b>{response[0]}</b> ℃\n'
                                          f'Ощущается как: <b>{response[1]}</b> ℃ {emoji_determinant(response[4])}',
                         parse_mode='html')
    except TypeError:
        bot.send_message(message.chat.id, ex1_type_err, parse_mode='html')


def _get_weather_min(message):
    """Функция делает запрос на API-сайт, выводит текущую минимальную температуру, записывает запрос в БД"""
    try:
        weather = site_api.get_response()
        response = weather(url, message.text, headers)
        data = [
            {'user_name': message.from_user.first_name, 'user_city': message.text, 'temp_now': 0, 'temp_like_now': 0,
             'other': response[2]}]
        db_write(db, History, data)

        bot.send_message(message.chat.id, f'Минимальная температура за сегодня в {message.text}: <b>{response[2]}</b> '
                                          f'℃ {emoji_determinant(response[4])}', parse_mode='html')
    except TypeError:
        bot.send_message(message.chat.id, ex1_type_err, parse_mode='html')


def _get_weather_max(message):
    """Функция делает запрос на API-сайт, выводит текущую максимальную температуру, записывает запрос в БД"""
    try:
        weather = site_api.get_response()
        response = weather(url, message.text, headers)
        data = [
            {'user_name': message.from_user.first_name, 'user_city': message.text, 'temp_now': 0, 'temp_like_now': 0,
             'other': response[3]}]
        db_write(db, History, data)

        bot.send_message(message.chat.id,
                         f'Максимальнаяя температура за сегодня в {message.text}: <b>{response[3]}</b> ℃'
                         f'{emoji_determinant(response[4])}', parse_mode='html')
    except TypeError:
        bot.send_message(message.chat.id, ex1_type_err, parse_mode='html')


def _history(message):
    """Функция выводит пользователю в чат мессенджера историю запросов"""
    db_read = crud.retrieve()

    retrieved = db_read(db, message.from_user.first_name, History, History.user_name, History.user_city,
                        History.temp_now,
                        History.temp_like_now, History.other)

    for idx, el in enumerate(reversed(retrieved)):
        if idx == 10:
            break
        bot.send_message(message.chat.id, f'{el.user_name, el.user_city, el.temp_now, el.temp_like_now, el.other}')


def _get_foto():
    '''Функция формирует путь к фото, возвращает фото и факт в словаре'''
    cur_path = os.path.dirname(__file__)
    new_path = os.path.join(cur_path, 'foto_pct')
    foto_list: list = [os.path.join(new_path, i_file) for i_file in os.listdir(new_path)]
    fact_list: list = [
        'Самая низкая температура в Москве за все время наблюдений – 17 июля 1940, было – 42,2 градуса',
        'В Берлине дождь идет в среднем 100 дней в году. В городе 175 музеев. Так что каждый дождливый день вы можете посещать разные музеи',
        'Самый холодный месяц в Москве – это февраль. Но, оказывается, что среднемесячная температура этого лютого месяца всего-то минус 6,7 градусов!',
        'В английском языке есть более 100 слов для обозначения дождя',
        'Минимальные месячные температуры в г. Казань наблюдались в январе 1891-го (-21 градус) и феврале 1954 года (-20 градусов)'
    ]

    foto_fact_date = dict(zip(foto_list, fact_list))
    return foto_fact_date


class TgInterface():
    @staticmethod
    def info(message):
        return _info(message)

    @staticmethod
    def get_weather(message):
        return _get_weather(message)

    @staticmethod
    def get_weather_max(message):
        return _get_weather_max(message)

    @staticmethod
    def get_weather_min(message):
        return _get_weather_min(message)

    @staticmethod
    def history(message):
        return _history(message)

    @staticmethod
    def get_foto():
        return _get_foto()


if __name__ == '__main__':
    TgInterface()
    _info()
    _get_weather()
    _get_weather_max()
    _get_weather_min()
    _history()
    _get_foto()
