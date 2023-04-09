""" Файл для сообщения 'привет'. """

from loader import bot
from telebot.types import Message
from loguru import logger
from database.history.message_history import save_message


@bot.message_handler(func=lambda message: message.text.lower() == "привет")
@logger.catch()
def test_hello_message(message: Message) -> None:
    """ Хендлер для сообщения 'привет'. """
    
    save_message(message)
    bot.reply_to(message, 'Привет!')
    