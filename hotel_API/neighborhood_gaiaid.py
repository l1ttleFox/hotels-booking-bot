""" Файл для функции получения id районов локации. """

from hotel_API.basic_request import api_request
from loguru import logger


@logger.catch()
def get_neighborhood_id(location: str) -> list:
    """ Функция получения id районов локации по названию локации. """
    
    neighborhoods = list()
    response = api_request("locations/v3/search", {"q": location, "locale": "ru_RU"}, "GET")
    objects = response["sr"]
    
    for i_obj in objects:
        if i_obj["type"] == "NEIGHBORHOOD" or i_obj["type"] == "CITY":
            i_neighborhood = {"name": i_obj["regionNames"]["displayName"], "id": i_obj["gaiaId"]}
            neighborhoods.append(i_neighborhood)
            logger.debug(f"Added neighborhood: {i_obj['regionNames']['displayName']} - {i_obj['gaiaId']}.")
            
    return neighborhoods
