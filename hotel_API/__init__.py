""" Пакет для работы с API hotels.com. """

from . import basic_request
from . import gaiaId
from . import request_location_id
from . import request_hottels_list
from . import detail_hotel_info
from . import neighborhood_gaiaid
from . import useful_hotels_list_request


__all__ = [
    "basic_request",
    "gaiaId",
    "request_location_id",
    "request_hottels_list",
    "detail_hotel_info",
    "neighborhood_gaiaid",
    "useful_hotels_list_request"
]
