import telebot
from settings import SiteSettings
from datetime import datetime
from tg_handler import TgInterface

tg_bot = SiteSettings()
bot = telebot.TeleBot(tg_bot.tg_api)
func_handler = TgInterface()
foto_fact: dict = func_handler.get_foto()
foto_fact_it = iter(foto_fact.items())


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
                         f'{answer} <b>{message.from_user.first_name}!</b> Вы можете воспользоваться кнопками '
                         f'ниже или использовать команды из меню\n', reply_markup=markup, parse_mode='html')
        bot.send_message(message.chat.id, '🌗')

    elif message.text == '/low':
        bot.send_message(message.chat.id, 'Напишите в каком городе хотите узнать минимальную температуру за сегодня:')
        bot.register_next_step_handler(message, func_handler.get_weather_min)
    elif message.text == '/high':
        bot.send_message(message.chat.id, 'Напишите в каком городе хотите узнать максимальную температуру за сегодня:')
        bot.register_next_step_handler(message, func_handler.get_weather_max)
    elif message.text == '/history':
        bot.send_message(message.chat.id, '<b>Ваши последние 10 запросов:</b>', parse_mode='html')
        func_handler.history(message)
    elif message.text == '/custom':
        bot.send_message(message.chat.id, '<b>Секретная информация о Вас</b>', parse_mode='html')
        bot.send_message(message.chat.id, message)
        with open('../site_api_weather/utils/cat.jpg', 'rb') as f:
            bot.send_photo(message.chat.id, f)
    else:
        bot.send_message(message.chat.id, 'Для того, чтобы повторить запрос воспользуйтесь кнопками или меню.')


@bot.message_handler(content_types=['text'])
def menu(message):
    '''Функция - обрабатывающая нажатие кнопок из меню, обрабатывает итератор'''

    if message.text.lower() == 'узнать погоду в городе':
        bot.send_message(message.chat.id, 'Напишите в чат бота название города на англиском или русском языке')
        bot.register_next_step_handler(message, func_handler.get_weather)
    elif message.text.lower() == 'информация по командам':
        func_handler.info(message)
    elif message.text.lower() == 'погода в фотографиях':
        global foto_fact_it
        global foto_fact
        try:
            path = next(foto_fact_it)
            with open(path[0], 'rb') as f:
                bot.send_message(message.chat.id, path[1])
                bot.send_photo(message.chat.id, f)
        except Exception:
            foto_fact_it = iter(foto_fact.items())

    else:
        bot.send_message(message.chat.id,
                         f'{message.from_user.first_name}, вы ввели: {message.text}, \n<b>Воспользуйтесь '
                         f'кнопками или используйте команды из меню</b>', parse_mode='html')


while True:
    try:
        if __name__ == '__main__':
            bot.polling(none_stop=True)
    except:
        continue
