from loader import bot
from loguru import logger
from hotel_API.detail_hotel_info import detail_info
from keyboards.inline.hotel_selection import detail_selection_keyboard
from handlers.custom_handlers.choosing_hotel import choosing_hotel


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
        
        bot.send_message(user_id, "Я рад, что Вы нашли то, что искали!")