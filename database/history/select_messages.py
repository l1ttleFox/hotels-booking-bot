""" Файл для функции, которая возвращает список из 10 последних команд пользователя. """

from loguru import logger
import sqlite3
from telebot.types import Message


@logger.catch()
def select_messages(message: Message) -> list:
    """ Функция выбирает из бд с командами пользователя последние 10. """
    
    with sqlite3.connect("database/db_files/history.db") as hist:
        hist.row_factory = sqlite3.Row
        cur = hist.cursor()
        
        message_chat_id = message.chat.id
        message_user_id = message.from_user.id
        cur.execute(f"""SELECT message, time FROM history
                        WHERE chat_id == {message_chat_id} AND user_id == {message_user_id}
                        ORDER BY id DESC""")
        data = cur.fetchmany(10)
        
        result = []
        for i_message in data:
            result.append(i_message["message"])
            
        return result
    