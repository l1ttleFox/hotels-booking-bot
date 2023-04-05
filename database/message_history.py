import sqlite3
from telebot.types import Message
from loguru import logger
from datetime import datetime


@logger.catch()
def save_message(message: Message) -> None:
    with sqlite3.connect("database/history.db") as hist:
        cur = hist.cursor()
        now = datetime.isoformat(datetime.now(), sep=" ")[:19]
        logger.debug(f"Message saved: '{message.text}', {message.chat.id}, {message.from_user.id}, '{now}'")
        cur.execute(f"INSERT INTO history (message, chat_id, user_id, time) VALUES ('{message.text}', {message.chat.id}, {message.from_user.id}, '{now}');")
        

