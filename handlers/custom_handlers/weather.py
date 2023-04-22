""" Файл для команды /weather. """

from loader import bot
from loguru import logger
from telebot.types import Message
from database.history.message_history import save_message
from weather_API.get_weather import get_weather
from telebot.apihelper import ApiTelegramException


@bot.message_handler(commands=["weather"])
@logger.catch()
def weather(message: Message) -> None:
    """ Хендлер для команды /weather. """
    
    try:
        logger.info("Weather command called.")
        save_message(message)
        location = message.text.replace("/weather ", "")
        
        bot.send_message(message.from_user.id, get_weather(location))
    except ApiTelegramException:
        bot.send_message(message.from_user.id, "Чтобы узнать погоду, используйте команду /weather <город>.")
        