""" Файл для команды /help. """

from loguru import logger
from telebot.types import Message
from loader import bot
from database.history.message_history import save_message


# TODO в этой команде выводить вообще все сообщения, или только осмысленные команды?
@bot.message_handler(commands=["help"])
@logger.catch()
def bot_start(message: Message) -> None:
    """ Хендлер для команды help. """
    
    save_message(message)
    bot.send_message(message.chat.id, "/survey - пройти опрос\n/history - история запросов\n/low - поиск отелей, начиная с дешевых\n/high - поиск отелей, начиная с дорогих\n/custom - Поиск отелей по Вашему диапазону")
