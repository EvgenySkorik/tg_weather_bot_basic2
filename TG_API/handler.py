# from tgbot import bot
#
#
# def _info(message):
#     '''Функция - выводящая в чат месенджера список команд'''
#
#     bot.send_message(message.chat.id, '<b>Список доступных команд:</b>\nВведите команду в чат месенджера',
#                      parse_mode='html')
#     bot.send_message(message.chat.id, '1. /start - запуск бота или возврат в основное меню')
#     bot.send_message(message.chat.id, '2. /low - узнать минимальную температура за сегодня')
#     bot.send_message(message.chat.id, '3. /high - узнать максимальную температура за сегодня')
#     bot.send_message(message.chat.id, '4. /custom - 2345')
#     bot.send_message(message.chat.id, '5. /history - Истоия запросов.')
#
#
#
# class TGbotInterface():
#
#     @staticmethod
#     def info():
#         return _info


if __name__=='main':
    _info()
    TGbotInterface()