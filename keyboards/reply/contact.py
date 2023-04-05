from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from loguru import logger


@logger.catch()
def request_contact() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(True, True)
    keyboard.add(KeyboardButton('Отправить контакт', request_contact=True))
    logger.info("Contact keyboard created.")
    return keyboard
