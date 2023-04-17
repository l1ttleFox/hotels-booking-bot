from loader import bot
from loguru import logger
from database.hotels.pull_hotels import pull_hotels
from database.travelers_info.pull_location_id import pull_location_id
from hotel_API.useful_hotels_list_request import useful_hotels_request
from keyboards.inline.hotel_selection import hotel_selection_keyboard


@logger.catch()
def choosing_hotel(message: dict):
    with bot.retrieve_data(int(message["user_id"]), int(message["chat_id"])) as data:
        logger.debug(data)
        hotel_counter = data["hotel_counter"]
        
        if hotel_counter == 0:
            useful_hotels_request(message["user_id"], message["sort"], message.get("filters"))
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
            