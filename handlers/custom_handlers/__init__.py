""" Файл для сборки пакета с кастомными обработчиками сообщений. """

from . import history
from . import low
from . import high
from . import custom
from . import survey
from . import collect_hotel_info
from . import callback
from . import choosing_hotel
from . import try_to_choose_hotel

__all__ = [
    "history",
    "low",
    "high",
    "custom",
    "survey",
    "collect_hotel_info",
    "try_to_choose_hotel",
    "callback",
    "choosing_hotel"
]
