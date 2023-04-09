""" Файл для команды /start. """

from loguru import logger
from telebot.types import Message
from loader import bot
from database.history.message_history import save_message


@bot.message_handler(commands=["start"])
@logger.catch()
def bot_start(message: Message) -> None:
    """ Хендлер для команды старт. """
    
    save_message(message)
    logger.debug("Command /start called.")
    
    bot.send_message(message.chat.id, "Привет! Я могу подобрать тебе отель в любой точке мира.")
