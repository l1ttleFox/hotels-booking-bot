""" Файл для хендлера "эхо". """

from loguru import logger
from telebot.types import Message
from loader import bot


@bot.message_handler(state=None)
@logger.catch()
def bot_echo(message: Message):
    """ Хендлер для неопознаных команд. """

    bot.reply_to(message, "Ошибка ввода. Введите /help для вывода руководства.")
