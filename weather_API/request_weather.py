""" Файл для функции запроса погоды от weather API. """

import requests
from requests.exceptions import RequestException
from weather_API.create_headers import create_weather_headers
from loguru import logger


@logger.catch()
def request_weather(location: str, days: int = 1) -> dict:
    """ Функция запроса текущей погоды по названию города. """
    
    try:
        headers = create_weather_headers(location, days)
        response = requests.get("http://api.weatherapi.com/v1/current.json", params=headers, timeout=10)
        logger.info("Trying to get response from weather API.")
        
        if response.status_code == requests.codes.ok:
            return response.json()
        
    except ConnectionError:
        logger.error("Connection lost.")
    except RequestException:
        logger.error("During the request something went wrong.")
        