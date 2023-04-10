""" Файл для удобной функции запроса списка отелей. """

from database.hotels.add_hotels_info import save_hotel_info
from hotel_API.request_hottels_list import get_hotels
from loguru import logger
from database.hotels.get_travelers_info import pull_traveler_info


@logger.catch()
def useful_hotels_request(user_id: str | int, sort: str) -> None:
    """ Удобная функция занесения в бд списка отелей по информации о путешественниках,
        занесённой в бд пользователем user_id.
        
        :arg sort: Передается тип сортировки. High - сначала дорогие, low - сначала дешевые.
        :arg user_id: Передается telegram id пользователя.
    """
    
    user_info = pull_traveler_info(str(user_id))
    if sort == "low":
        user_info["sort"] = "PRICE_LOW_TO_HIGH"
    elif sort == "high":
        user_info["sort"] = "PRICE_HIGH_TO_LOW"
        
    raw_response = get_hotels(user_info)
    save_hotel_info(raw_response)
    