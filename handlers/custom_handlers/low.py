""" Файл для команды /low."""

from loader import bot
from loguru import logger
from telebot.types import Message
from database.history.message_history import save_message
from states.hotel_info import HotelInfoState
from handlers.custom_handlers.choosing_hotel import choosing_hotel


@bot.message_handler(commands=["low"], state=HotelInfoState.ready)
@logger.catch()
def low(message: Message) -> None:
    """ Хендлер для команды /low, когда вся информация о путешественниках уже собрана."""
    
    logger.info("/low command called.")
    save_message(message)
    
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["hotel_counter"] = 0
    
    formatted_message = {
        "user_id": message.from_user.id,
        "chat_id": message.chat.id,
        "sort": "low"}
    choosing_hotel(formatted_message)
