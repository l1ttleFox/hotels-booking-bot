""" Файл для создания клавиатуры с кнопками выбора отеля. """

from loguru import logger
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message


@logger.catch()
def hotel_selection_keyboard(hotel_id: str | int, message: dict) -> InlineKeyboardMarkup:
    """ Функция создаёт кнопки 'следующий отель' и 'подробнее об отеле'. """
    
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="Больше информации",
                                      callback_data=f"SH_{hotel_id} {message['user_id']} {message['chat_id']}"))
    
    keyboard.add(InlineKeyboardButton(text="Дальше",
                                      callback_data=f"SH_next {message['user_id']} {message['chat_id']}"))
    
    logger.info("Select hotel keyboard created.")
    return keyboard


@logger.catch()
def detail_selection_keyboard(message: dict) -> InlineKeyboardMarkup:
    """ Функция создаёт кнопки 'следующий отель' и 'стоп'. """
    
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="Мне подходит",
                                      callback_data=f"SH_next {message['user_id']} {message['chat_id']}"))
    
    keyboard.add(InlineKeyboardButton(text="Дальше",
                                      callback_data=f"SH_next {message['user_id']} {message['chat_id']}"))
    
    logger.info("Select hotel keyboard created.")
    return keyboard