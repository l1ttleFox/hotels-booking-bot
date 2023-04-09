""" Файл для функции получения id локации по названию локации. """

from .gaiaId import get_gaiaid
from . import basic_request
from loguru import logger


@logger.catch()
def get_location_id(location: str) -> str:
    """ Функция получения id локации по названию локации. """
    
    response = basic_request.api_request("locations/v3/search", {"q": location, "locate": "ru_Ru"}, "GET")
    location_id = get_gaiaid(response)
    logger.debug(f"gaiaId: {location_id}")
    
    return location_id
