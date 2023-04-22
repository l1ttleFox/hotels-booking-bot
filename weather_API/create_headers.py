""" Файл для создания параметров запроса к weather API. """

from config_data.config import WEATHER_API_KEY
from loguru import logger


@logger.catch()
def create_weather_headers(location: str, days=1) -> dict:
    """ Функция создания параметров запроса прогноза погоды. """
    
    weather_headers = {
        "key": WEATHER_API_KEY,
        "q": location,
        "days": days,
        "lang": "ru"
    }
    return weather_headers
