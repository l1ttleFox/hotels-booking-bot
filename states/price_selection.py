""" Файл для хранения объекта стадии пользователя во время выбора отеля. """

from telebot.handler_backends import State, StatesGroup
from loguru import logger


class PriceSelectionState(StatesGroup):
    """ Класс для хранения объекта стадии пользователя во запроса максимальной и минимальной цены отеля. Родитель: StatesGroup. """
    
    min_price = State()
    max_price = State()
    ready = State()
