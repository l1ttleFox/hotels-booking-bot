""" Файл для хранения объекта со стадией пользователя во время запроса информации. """

from telebot.handler_backends import State, StatesGroup
from loguru import logger


class UserInfoState(StatesGroup):
    """ Класс для хранения состояния пользователя в опросе. Родитель: StatesGroup. """
    
    name = State()
    age = State()
    country = State()
    city = State()
    phone_number = State()


logger.info("Class 'UserInfoState' created.")
