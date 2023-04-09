""" Файл для функции получения id локации из файла json. """

from loguru import logger


@logger.catch()
def get_gaiaid(response: dict) -> str:
    """ Функция возвращает id локации из сырого ответа от API. """
    
    temp = response.get("sr")[0]
    location_id = temp.get("gaiaId")
    return location_id