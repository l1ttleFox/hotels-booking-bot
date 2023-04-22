""" Файл для функции получения погоды в виде текста по названию города. """

from weather_API.request_weather import request_weather
from weather_API.format_weather import format_weather
from loguru import logger


@logger.catch()
def get_weather(location: str, days: int = 1) -> str:
    """ Функция получения погоды по названию города в текстовом формате. """
    
    try:
        raw_response = request_weather(location, days)
        weather = format_weather(raw_response)
        
        return f"""Погода в городе {weather['name']}
               Температура воздуха: {weather['temperature']} °C
               Ощущается: {weather['fells_like']} °C
               Скорость ветра: {weather['wind_speed']} км/ч
               УФ индекс: {weather['uv']}
               Описание погоды: {weather['condition']}
                """
    except TypeError:
        pass
    