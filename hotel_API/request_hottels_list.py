""" Файл для функции получения списка отелей по id локации. """

from hotel_API import basic_request
from loguru import logger


@logger.catch()
def get_hotels(user_info: dict):
    """ Функция возвращает сырой ответ от API со списком отелей по id локации. """
    
    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "ru_RU",
        "siteId": 300000001,
        "destination": {"regionId": str(user_info["location_id"])},
        "checkInDate": {"day": int(user_info["check_in_date"][2]),
                        "month": int(user_info["check_in_date"][1]),
                        "year": int(user_info["check_in_date"][0])},
        "checkOutDate": {"day": int(user_info["check_out_date"][2]),
                         "month": int(user_info["check_out_date"][1]),
                         "year": int(user_info["check_out_date"][0])},
        "rooms": user_info["rooms"],
        "resultsStartingIndex": 0,
        "resultsSize": 100,
        "sort": user_info["sort"],
        "filters": {"availableFilter": "SHOW_AVAILABLE_ONLY"}
    }
    
    logger.debug(payload)
    response = basic_request.api_request("properties/v2/list", payload, "POST")
    return response
