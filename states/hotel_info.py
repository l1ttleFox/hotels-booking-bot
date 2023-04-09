""" Файл для хранения объекта стадии пользователя во время сбора информации о путешественниках. """

from telebot.handler_backends import State, StatesGroup
from loguru import logger


class HotelInfoState(StatesGroup):
    """ Класс для хранения объекта стадии пользователя во время выбора отеля. Родитель: StatesGroup. """
    
    start = ()
    location = State()
    check_in_date = State()
    check_out_date = State()
    adults = State()
    kids = State()
    kids_age = State()
    ready = State()


logger.info("Class 'HotelInfoState' created.")
