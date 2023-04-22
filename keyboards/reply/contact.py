""" Файл для создания клавиатуры с кнопкой 'отправить номер телефона'. """

from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from loguru import logger


@logger.catch()
def request_contact() -> ReplyKeyboardMarkup:
    """ Функция создаёт клавиатуру для запроса номера телефона у пользователя. """
    
    keyboard = ReplyKeyboardMarkup(True, True)
    keyboard.add(KeyboardButton("Отправить контакт", request_contact=True))
    
    return keyboard
