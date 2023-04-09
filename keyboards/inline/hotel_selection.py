""" Файл для создания клавиатуры с кнопками выбора отеля. """

from loguru import logger
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


@logger.catch()
def hotel_selection_keyboard(hotel_id: str | int) -> InlineKeyboardMarkup:
    """ Функция создаёт кнопки 'следующий отель' и 'подробнее об отеле'. """
    
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="Больше информации",
                                      callback_data=f"SH_{hotel_id}"))
    
    keyboard.add(InlineKeyboardButton(text="Дальше",
                                      callback_data=f"SH_next"))
    
    logger.info("Select hotel keyboard created.")
    return keyboard


@logger.catch()
def detail_selection_keyboard() -> InlineKeyboardMarkup:
    """ Функция создаёт кнопки 'следующий отель' и 'стоп'. """
    
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="Мне подходит",
                                      callback_data=f"SH_stop"))
    
    keyboard.add(InlineKeyboardButton(text="Дальше",
                                      callback_data=f"SH_next"))
    
    logger.info("Select hotel keyboard created.")
    return keyboard