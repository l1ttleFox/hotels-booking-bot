""" Файл для функции получения id районов локации. """

from hotel_API.basic_request import api_request
from loguru import logger


@logger.catch()
def get_neighborhood_id(location: str) -> list:
    """ Функция получения id районов локации по названию локации. """
    
    neighborhoods = list()
    response = api_request("locations/v3/search", {"q": location, "locale": "ru_RU"}, "GET")
    objects = response["sr"]
    
    for i_object in objects:
        if i_object["type"] == "NEIGHBORHOOD" or i_object["type"] == "CITY":
            i_neighborhood = {"name": i_object["regionNames"]["displayName"], "id": i_object["gaiaId"]}
            neighborhoods.append(i_neighborhood)
            logger.debug(f"Added neighborhood: {i_object['regionNames']['displayName']} - {i_object['gaiaId']}.")
            
    return neighborhoods
