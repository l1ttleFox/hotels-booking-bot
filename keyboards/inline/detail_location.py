""" Файл для создания клавиатуры с локациями для уточнения. """

from loader import bot
from loguru import logger
from states.hotel_info import HotelInfoState
from database.history.message_history import save_message
from hotel_API.neighborhood_gaiaid import get_neighborhood_id
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

user_message: Message = None


@bot.callback_query_handler(func=lambda call: call.data.isdigit())
def save_location_id(call) -> None:
    """ Функция принимает нажатие на кнопку с точной локацией. """
    
    global user_message
    save_message(user_message)

    bot.send_message(user_message.from_user.id, "Я запомнил. Теперь введи дату заселения (гггг.мм.дд).")
    bot.set_state(user_message.from_user.id, HotelInfoState.check_in_date, user_message.chat.id)
    
    with bot.retrieve_data(user_message.from_user.id, user_message.chat.id) as data:
        data["detail_location_id"] = call.data


@logger.catch()
def request_detail_location(message: Message) -> InlineKeyboardMarkup:
    """ Функция создаёт кнопки с точными названиями локации и callback'ом id. """
    
    global user_message
    user_message = message
    neighborhoods = get_neighborhood_id(message.text)
    
    keyboard = InlineKeyboardMarkup()
    for i_neighborhood in neighborhoods:
        keyboard.add(InlineKeyboardButton(text=i_neighborhood["name"],
                                          callback_data=i_neighborhood["id"]))
    
    logger.info("Detailed locations keyboard created.")
    return keyboard
