""" Файл для сборки пакета с кастомными обработчиками сообщений. """

from . import history
from . import low
from . import high
from . import custom
from . import survey
from . import collect_hotel_info

__all__ = ["history", "low", "high", "custom", "survey", "collect_hotel_info"]
