""" Файл для функции запроса информации об отелях. """

from config_data.config import headers
from loguru import logger
import requests
from requests.exceptions import RequestException


@logger.catch()
def api_request(method_endswith: str, params: dict, method_type: str) -> dict:
    """ Удобная функция для любых запросов с API отелей. """
    
    url = f"https://hotels4.p.rapidapi.com/{method_endswith}"
    logger.info(f"Trying to get response from {url}.")
    
    if method_type == "GET":
        return get_request(url=url, params=params)
    else:
        return post_request(url=url, params=params)


@logger.catch()
def get_request(url: str, params: dict) -> dict:
    """ Функция get-запроса к API отелей. """
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        logger.debug("GET response caught.")
        logger.debug(f"Status code:{response.status_code}")
        if response.status_code == requests.codes.ok:
            return response.json()
    
    except ConnectionError:
        logger.error("Connection lost.")
    except RequestException:
        logger.error("During the request something went wrong.")


@logger.catch()
def post_request(url: str, params: dict) -> dict:
    """ Функция post-запроса к API отелей. """
    
    try:
        response = requests.post(url, json=params, headers=headers, timeout=10)
        logger.debug("POST response caught.")
        logger.debug(f"Status code:{response.status_code}")
        if response.status_code == requests.codes.ok:
            return response.json()
    
    except ConnectionError:
        logger.error("Connection lost.")
    except RequestException:
        logger.error("During request something went wrong.")
