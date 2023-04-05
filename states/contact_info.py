""" Файл для хранения объекта с пользовательской информацией. """

from telebot.handler_backends import State, StatesGroup
from loguru import logger


class UserInfoState(StatesGroup):
    name = State()
    age = State()
    country = State()
    city = State()
    phone_number = State()


logger.info("Class 'UserInfoState' created.")
