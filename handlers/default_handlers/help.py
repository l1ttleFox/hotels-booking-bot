""" Файл для команды /help. """

from loguru import logger
from telebot.types import Message
from loader import bot
from database.history.message_history import save_message


@bot.message_handler(commands=["help"])
@logger.catch()
def bot_start(message: Message) -> None:
    """ Хендлер для команды help. """
    
    save_message(message)
    bot.send_message(message.chat.id, """/survey - пройти опрос
                                         /history - история запросов
                                         /low - поиск отелей, начиная с дешевых
                                         /high - поиск отелей, начиная с дорогих
                                         /custom - поиск отелей по Вашему диапазону
                                         /weather <город> - текущая погода в городе
                                      """)
