""" Файл для подгрузки токена бота и API. """

import os
import dotenv
from loguru import logger

if not dotenv.find_dotenv():
    logger.critical(".env file does not exists in root directory.")
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    dotenv.load_dotenv()
    logger.info(".env bot token loaded.")

BOT_TOKEN = os.getenv("BOT_TOKEN")
RAPID_API_KEY = os.getenv("RAPID_API_KEY")
DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("help", "Вывести справку"),
    ("helloworld", "Проверить бота"),
    ("survey", "Пройти опрос"),
    ("low", "Поиск отелей с дешёвых"),
    ("history", "история сообщений")
)
headers = {
    "X-RapidAPI-Key": RAPID_API_KEY,
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}
