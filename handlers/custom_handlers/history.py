"""Тут будет реализация команды /history."""

from loader import bot
from loguru import logger
from telebot.types import Message
from database.select_messages import select_messages


@bot.message_handler(commands=["history"])
def bot_history(message: Message) -> None:
    last_messages = select_messages(message)
    last_messages = "\n".join(last_messages)
    bot.send_message(message.chat.id, f"Вот твои последние команды:\n{last_messages}")