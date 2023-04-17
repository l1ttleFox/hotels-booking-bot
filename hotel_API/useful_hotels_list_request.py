""" Файл для удобной функции запроса списка отелей. """

from database.hotels.add_hotels_info import save_hotel_info
from hotel_API.request_hottels_list import get_hotels
from loguru import logger
from database.hotels.get_travelers_info import pull_traveler_info


@logger.catch()
def useful_hotels_request(user_id: str | int, sort: str, filters=None) -> None:
    """ Удобная функция занесения в бд списка отелей по информации о путешественниках,
        занесённой в бд пользователем user_id.
        
        :arg sort: Передается тип сортировки. High - сначала дорогие, low - сначала дешевые.
        :arg user_id: Передается telegram id пользователя.
        :arg filters: Передается фильтр цен. Если аргумент не задан, фильтра по ценам нет.
    """

    if filters is None:
        filters = {"availableFilter": "SHOW_AVAILABLE_ONLY"}
        
    user_info = pull_traveler_info(str(user_id))
    if sort == "low":
        logger.debug("low")
        user_info["sort"] = "PRICE_LOW_TO_HIGH"
    elif sort == "high":
        logger.debug("high")
        user_info["sort"] = "PRICE_HIGH_TO_LOW"
    user_info["filters"] = filters
        
    raw_response = get_hotels(user_info)
    save_hotel_info(raw_response)
    