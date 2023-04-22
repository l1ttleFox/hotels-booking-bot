""" Файл для создания клавиатуры с локациями для уточнения. """

from loguru import logger
from hotel_API.neighborhood_gaiaid import get_neighborhood_id
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message


@logger.catch()
def request_detail_location(message: Message) -> InlineKeyboardMarkup:
    """ Функция создаёт кнопки с точными названиями локации и callback'ом id. """
    
    neighborhoods = get_neighborhood_id(message.text)
    
    keyboard = InlineKeyboardMarkup()
    for i_neighborhood in neighborhoods:
        keyboard.add(InlineKeyboardButton(text=i_neighborhood["name"],
                                          callback_data=f"{i_neighborhood['id']} {message.from_user.id} {message.chat.id}"))
    
    return keyboard
