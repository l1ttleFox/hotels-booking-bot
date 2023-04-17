""" Файл для команды /custom."""

from loader import bot
from loguru import logger
from telebot.types import Message
from database.history.message_history import save_message
from states.hotel_info import HotelInfoState
from states.price_selection import PriceSelectionState
from handlers.custom_handlers.choosing_hotel import choosing_hotel
from handlers.custom_handlers.collect_hotel_info import start_collecting_hotel_info


@bot.message_handler(commands=["custom"], state=PriceSelectionState.ready)
@logger.catch()
def try_custom(message: Message) -> None:
    """ Хендлер для команд подбора отеля, когда информация о путешественниках еще не собрана."""
    
    logger.info("/custom command called.")
    save_message(message)
    
    bot.send_message(message.from_user.id, "Я могу подобрать отель, но сначала мне нужно узнать подробности.")
    bot.set_state(message.from_user.id, HotelInfoState.start, message.chat.id)
    
    start_collecting_hotel_info(message)


@bot.message_handler(state=PriceSelectionState.min_price)
@logger.catch()
def get_max_price(message: Message) -> None:
    """ Хендлер для команды /custom. Стадия запроса максимальной цены. """
    
    try:
        logger.info("/custom command called.")
        save_message(message)
        
        bot.send_message(message.from_user.id, "А максимальная? (тоже в долларах)")
        bot.set_state(message.from_user.id, PriceSelectionState.max_price, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["min"] = int(message.text)
            data["first_message"] = "custom"
    
    except ValueError:
        logger.warning("Minimal price is not integer.")
        bot.send_message(message.from_user.id, "Попробуйте еще раз.")


@bot.message_handler(state=PriceSelectionState.max_price)
@logger.catch()
def custom_ready(message: Message) -> None:
    """ Хендлер для команды /custom. Стадия окончания опроса. """
    
    try:
        logger.info("/custom command called.")
        save_message(message)
        
        bot.send_message(message.from_user.id, "Я запомнил.")
        bot.set_state(message.from_user.id, HotelInfoState.start, message.chat.id)
        bot.set_state(message.from_user.id, PriceSelectionState.ready, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["max"] = int(message.text)
        try_custom(message)
    
    except ValueError:
        logger.warning("Minimal price is not integer.")
        bot.send_message(message.from_user.id, "Попробуйте еще раз.")


@bot.message_handler(commands=["custom"], state=HotelInfoState.ready)
@logger.catch()
def custom(message: Message) -> None:
    """ Хендлер для команды /custom, когда вся информация о путешественниках уже собрана."""
    
    logger.info("/custom command called.")
    save_message(message)
    
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["hotel_counter"] = 0
    
        formatted_message = {
            "user_id": message.from_user.id,
            "chat_id": message.chat.id,
            "sort": "low",
            "filters": {
                "availableFilter": "SHOW_AVAILABLE_ONLY",
                "price": {"max": data['max'], "min": data['min']}
            }
        }
    choosing_hotel(formatted_message)


@bot.message_handler(commands=["custom"])
@logger.catch()
def get_min_price(message: Message) -> None:
    """ Хендлер для команды /custom. Стадия запроса минимальной цены. """
    
    logger.info("/custom command called.")
    save_message(message)
    
    bot.send_message(message.from_user.id, "Хорошо, какая минимальная цена? (в долларах)")
    bot.set_state(message.from_user.id, PriceSelectionState.min_price, message.chat.id)