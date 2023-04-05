""" Файл для функции, которая возвращает список из 10 последних команд пользователя. """

from loguru import logger
import sqlite3
from telebot.types import Message


def select_messages(message: Message) -> list:
    with sqlite3.connect("database/history.db") as hist:
        hist.row_factory = sqlite3.Row
        cur = hist.cursor()
        
        message_chat_id = message.chat.id
        message_user_id = message.from_user.id
        cur.execute(f"""SELECT message, time FROM history WHERE chat_id == {message_chat_id} AND user_id == {message_user_id} ORDER BY id DESC""")
        data = cur.fetchmany(10)
        
        result = []
        for i in data:
            logger.debug(f'{i["message"]}:{i["time"]}')
            result.append(i["message"])
        return result