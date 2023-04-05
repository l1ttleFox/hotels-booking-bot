""" Тут будет реализация команды /help. """

from loguru import logger
from telebot.types import Message
from loader import bot
from database.message_history import save_message


@bot.message_handler(commands=["help"])
@logger.catch()
def bot_start(message: Message) -> None:
    """ Хендлер для команды help. """
    save_message(message)
    
    bot.send_message(message.chat.id, "/survey - пройти опрос\n/history - история запросов.")