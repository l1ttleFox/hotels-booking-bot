""" Файл для команды /low."""

from loader import bot
from loguru import logger
from telebot.types import Message
from database.hotels.pull_hotels import pull_hotels
from database.history.message_history import save_message
from database.travelers_info.pull_location_id import pull_location_id
from states.hotel_info import HotelInfoState
from hotel_API.useful_hotels_list_request import useful_hotels_request
from hotel_API.detail_hotel_info import detail_info
from keyboards.inline.hotel_selection import hotel_selection_keyboard, detail_selection_keyboard


@bot.message_handler(commands=["low"], state=HotelInfoState.ready)
@logger.catch()
def low(message: Message) -> None:
    """ Хендлер для команды /low, когда вся информация о путешественниках уже собрана."""
    
    logger.info("/low command called.")
    save_message(message)
    
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["hotel_counter"] = 0
    
    formatted_message = {
        "user_id": message.from_user.id,
        "chat_id": message.chat.id}
    choosing_hotel(formatted_message)


@bot.message_handler(commands=["low"])
@logger.catch()
def low(message: Message) -> None:
    """ Хендлер для команды /low, когда информация о путешественниках еще не собрана."""
    
    logger.info("/low command called.")
    save_message(message)
    
    bot.send_message(message.from_user.id, "Я могу подобрать отель, но сначала мне нужно узнать подробности.")
    bot.send_message(message.from_user.id, "Используйте команду /start, чтобы начать опрос.")
    
    bot.set_state(message.from_user.id, HotelInfoState.start, message.chat.id)


@bot.callback_query_handler(lambda call: call.data.split()[0].startswith("SH_"))
def callback_handler(call):
    """ Колбэк-обработчик кнопок. """
    
    logger.debug(call.data)
    callback = call.data.split()[0].replace("SH_", "")
    user_id = call.data.split()[1]
    chat_id = call.data.split()[2]
    if callback.isdigit():
        """ Тут вызываем функцию которая выводит конкретную информацию об отеле. """
        
        hotel_info = detail_info(callback)
        for i_image in hotel_info["images"]:
            bot.send_photo(user_id, i_image)
        
        formatted_message = {
            "user_id": user_id,
            "chat_id": chat_id}
        
        bot.send_message(user_id, f"Название отеля: {hotel_info['name']}\n"
                                               f"Рейтинг: {hotel_info['score']}\n"
                                               f"Адрес: {hotel_info['address']}\n"
                                               f"Описание: {hotel_info['tagline']}\n",
                         reply_markup=detail_selection_keyboard(formatted_message))
    
    elif callback == "next":
        """ Тут реализация кнопки 'дальше'. """
        
        formatted_message = {
            "user_id": user_id,
            "chat_id": chat_id}
        choosing_hotel(formatted_message)
    
    elif callback == "stop":
        """ Реализация кнопки stop. """
        
        bot.send_message(user_id, "Я рад, что вы нашли то, что искали!")


@logger.catch()
def choosing_hotel(message: dict):
    with bot.retrieve_data(int(message["user_id"]), int(message["chat_id"])) as data:
        hotel_counter = data["hotel_counter"]
        
        if hotel_counter == 0:
            useful_hotels_request(message["user_id"])
            hotels = pull_hotels(pull_location_id(str(message["user_id"])))
            data["hotels"] = hotels
        else:
            hotels = data["hotels"]
            
        try:
            hotel_id, hotel_name, price, image = hotels[hotel_counter]
            if image:
                bot.send_photo(message["user_id"], image)
            
            bot.send_message(message["user_id"],
                             f"Название отеля: {hotel_name},\n"
                             f"Цена за ночь: {price}",
                             reply_markup=hotel_selection_keyboard(hotel_id, message))
            data["hotel_counter"] += 1
        
        except IndexError:
            bot.send_message(message["user_id"], "Вы просмотрели все отели.")
