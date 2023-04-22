""" Файл для команд /high и /low, когда информация о путешественниках еще не собрана. """

from loader import bot
from loguru import logger
from telebot.types import Message
from database.history.message_history import save_message
from states.hotel_info import HotelInfoState
from handlers.custom_handlers.collect_hotel_info import start_collecting_hotel_info


@bot.message_handler(commands=["low"])
@logger.catch()
def low(message: Message) -> None:
    """ Хендлер для команд подбора отеля, когда информация о путешественниках еще не собрана."""
    
    logger.info("/low command called.")
    save_message(message)
    
    bot.send_message(message.from_user.id, "Я могу подобрать отель, но сначала мне нужно узнать подробности.")
    
    bot.set_state(message.from_user.id, HotelInfoState.start, message.chat.id)
    start_collecting_hotel_info(message)
    

@bot.message_handler(commands=["high"])
@logger.catch()
def high(message: Message) -> None:
    """ Хендлер для команд подбора отеля, когда информация о путешественниках еще не собрана."""
    
    logger.info("/high command called.")
    save_message(message)
    
    bot.send_message(message.from_user.id, "Я могу подобрать отель, но сначала мне нужно узнать подробности.")
    
    bot.set_state(message.from_user.id, HotelInfoState.start, message.chat.id)
    start_collecting_hotel_info(message)
