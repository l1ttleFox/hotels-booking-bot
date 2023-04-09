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

# TODO так можно оставить глобальные переменные?
user_message_instance: Message = None
hotels_list: list = list()
next_hotel: tuple = None
hotel_counter: int = 1


@bot.message_handler(commands=["low"], state=HotelInfoState.ready)
@logger.catch()
def low(message: Message) -> None:
    """ Хендлер для команды /low, когда вся информация о путешественниках уже собрана."""
    
    global hotels_list, user_message_instance
    user_message_instance = message
    logger.info("/low command called.")
    save_message(message)
    
    useful_hotels_request(message.from_user.id)
    hotels_list = pull_hotels(pull_location_id(str(message.from_user.id)))
    first_hotel = hotels_list[0]
    
    if first_hotel[3]:
        bot.send_photo(message.from_user.id, first_hotel[3])
    bot.send_message(message.from_user.id, f"Название отеля: {first_hotel[1]},\n"
                     f"Цена за ночь: {first_hotel[2]}",
                     reply_markup=hotel_selection_keyboard(first_hotel[0]))
    
    
@bot.message_handler(commands=["low"])
@logger.catch()
def low(message: Message) -> None:
    """ Хендлер для команды /low, когда информация о путешественниках еще не собрана."""
    
    global user_message_instance
    logger.info("/low command called.")
    save_message(message)
    user_message_instance = message
    
    bot.send_message(message.from_user.id, "Я могу подобрать отель, но сначала мне нужно узнать подробности.")
    bot.send_message(message.from_user.id, "Используйте команду /start, чтобы начать опрос.")

    bot.set_state(message.from_user.id, HotelInfoState.start, message.chat.id)
   

@bot.callback_query_handler(lambda call: call.data.startswith("SH_"))
def callback_handler(call):
    """ Колбэк-обработчик кнопок. """
    global hotel_counter, user_message_instance
    
    callback = call.data.replace("SH_", "")
    logger.debug(callback)
    if callback.isdigit():
        """ Тут вызываем функцию которая выводит конкретную информацию об отеле. """
        
        hotel_info = detail_info(callback)
        for i_image in hotel_info["images"]:
            bot.send_photo(user_message_instance.from_user.id, i_image)
            
        bot.send_message(user_message_instance.from_user.id, f"Название отеля: {hotel_info['name']}\n"
                                                             f"Рейтинг: {hotel_info['score']}\n"
                                                             f"Адрес: {hotel_info['address']}\n"
                                                             f"Описание: {hotel_info['tagline']}\n",
                         reply_markup=detail_selection_keyboard())

    elif callback == "next":
        """ Тут реализация кнопки 'дальше'. """
        
        try:
            hotel_id, hotel_name, price, image = hotels_list[hotel_counter]
            if image:
                bot.send_photo(user_message_instance.from_user.id, image)
            bot.send_message(user_message_instance.from_user.id,
                             f"Название отеля: {hotel_name},\n"
                             f"Цена за ночь: {price}",
                             reply_markup=hotel_selection_keyboard(hotel_id))
            hotel_counter += 1
            
        except IndexError:
            bot.send_message(user_message_instance.from_user.id, "Вы просмотрели все отели.")
    
    elif callback == "stop":
        """ Реализация кнопки stop. """
        
        bot.send_message(user_message_instance.from_user.id, "Я рад, что вы нашли то, что искали!")