""" Файл для хранения объекта стадии пользователя во время выбора отеля. """
""" Еще нигде не используется """

from telebot.handler_backends import State, StatesGroup
from loguru import logger


class HotelSelectionState(StatesGroup):
    """ Класс для хранения объекта стадии пользователя во время выбора отеля. Родитель: StatesGroup. """
    
    start = ()
    next_hotel = State()
    more_info = State()


logger.info("Class 'HotelSelectionState' created.")
