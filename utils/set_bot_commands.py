""" Файл для создания в боте меню с командами. """

from telebot.types import BotCommand
from config_data.config import DEFAULT_COMMANDS
from loguru import logger

@logger.catch()
def set_default_commands(bot):
    bot.set_my_commands(
        [BotCommand(*i) for i in DEFAULT_COMMANDS]
    )
    logger.info("Bot's command menu created")