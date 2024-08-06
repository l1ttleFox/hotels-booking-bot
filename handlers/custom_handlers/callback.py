""" Файл для работы с callback информацией с кнопок. """

from loader import bot
from loguru import logger
from hotel_API.detail_hotel_info import detail_info
from keyboards.inline.hotel_selection import detail_selection_keyboard
from handlers.custom_handlers.choosing_hotel import choosing_hotel
from states.hotel_info import HotelInfoState


@bot.callback_query_handler(lambda call: call.data.split()[0].startswith("SH_"))
@logger.catch()
def callback_handler(call) -> None:
    """ Колбэк-обработчик кнопок. """
    
    callback = call.data.split()[0].replace("SH_", "")
    user_id = call.data.split()[1]
    chat_id = call.data.split()[2]
    if callback.isdigit():
        """ Тут вызываем функцию которая выводит конкретную информацию об отеле. """
        
        hotel_info = detail_info(callback)
        ten_hotels_counter = 0
        for i_image in hotel_info["images"]:
            if ten_hotels_counter == 10:
                break
            ten_hotels_counter += 1
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
        
        bot.send_message(user_id, "Я рад, что Вы нашли то, что искали!")


@bot.callback_query_handler(state=HotelInfoState.location, func=lambda call: call.data.split()[0].isdigit())
@logger.catch()
def save_location_id(call) -> None:
    """ Функция принимает нажатие на кнопку с точной локацией. """
    
    location_id = call.data.split()[0]
    tg_user_id = int(call.data.split()[1])
    tg_chat_id = int(call.data.split()[2])
    
    with bot.retrieve_data(tg_user_id, tg_chat_id) as data:
        data["detail_location_id"] = location_id
        
    bot.send_message(tg_user_id, "Я запомнил. Теперь введите дату заселения (гггг.мм.дд).")
    bot.set_state(tg_user_id, HotelInfoState.check_in_date, tg_chat_id)
    