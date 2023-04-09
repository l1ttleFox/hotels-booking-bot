""" Файл для тестовой команды 'helloworld'. """

from loader import bot
from telebot.types import Message
from loguru import logger
from database.history.message_history import save_message


@bot.message_handler(commands=["helloworld"])
@logger.catch()
def test_message(message: Message) -> None:
    """ Хендлер для тестовой команды 'helloworld'. """
    
    save_message(message)
    bot.send_message(message.chat.id, 'Если вы видите это сообщение, значит все работает.')
    