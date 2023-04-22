""" Файл для обработки сырого запроса от weather API. """

from loguru import logger


@logger.catch()
def format_weather(raw_response: dict) -> dict:
    """ Функция для обработки сырого запроса weather API. """
    
    try:
        weather = dict()
        weather["name"] = raw_response["location"]["name"]
        weather["temperature"] = raw_response["current"]["temp_c"]
        weather["fells_like"] = raw_response["current"]["feelslike_c"]
        weather["condition"] = raw_response["current"]["condition"]["text"]
        weather["wind_speed"] = raw_response["current"]["wind_kph"]
        weather["uv"] = raw_response["current"]["uv"]
        
        return weather
    except TypeError:
        pass
    