""" Файл для "инициализации" бота. """

from telebot import TeleBot
from telebot.storage import StateMemoryStorage
from config_data import config
from loguru import logger


logger.add("bot.log",
           format="{time} {level} {message}",
           level="DEBUG",
           rotation="100 KB",
           compression="zip"
           )

storage = StateMemoryStorage()
logger.info("Created state memory storage.")
bot = TeleBot(token=config.BOT_TOKEN, state_storage=storage)
logger.success("Bot initialized.")
