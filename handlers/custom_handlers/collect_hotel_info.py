""" Файл для сценария сбора информации об отеле. """

from loader import bot
from telebot.types import Message
from states.hotel_info import HotelInfoState
from keyboards.inline.detail_location import request_detail_location
from loguru import logger
from database.history.message_history import save_message
from database.travelers_info.add_travelers_info import save_travelers_info
# from handlers.custom_handlers.low import low
# from handlers.custom_handlers.high import high
# from handlers.custom_handlers.custom import custom


@bot.message_handler(state=HotelInfoState.start, commands=["start"])
@logger.catch()
def start_collecting_hotel_info(message: Message) -> None:
    """ Хендлер для состояния старта запроса информации. """
    
    logger.info("Start state in collecting hotel info started.")
    save_message(message)
    
    bot.set_state(message.from_user.id, HotelInfoState.location, message.chat.id)
    bot.send_message(message.from_user.id, f"{message.from_user.username}, в каком городе планируете остановиться?")


@bot.message_handler(state=HotelInfoState.location)
@logger.catch()
def get_location(message: Message) -> None:
    """ Хендлер для состояния запроса названия локации. """
    
    logger.info("Location state in collecting hotel info started.")
    save_message(message)
    
    bot.send_message(message.from_user.id,
                     "Уточните, пожалуйста.",
                     reply_markup=request_detail_location(message))
    
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["location"] = message.text
        data["user_id"] = message.from_user.id


@bot.message_handler(state=HotelInfoState.check_in_date)
@logger.catch()
def get_check_in_date(message: Message) -> None:
    """ Хендлер для состояния запроса даты заезда. """
    
    logger.info("Check in date state in collecting hotel info started.")
    save_message(message)
    
    try:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            if len(message.text.split(".")) != 3:
                raise TypeError("Invalid check in date.")
            date = list()
            for i_element in message.text.split("."):
                if not i_element.isdigit():
                    raise ValueError("Check in date is not integer.")
                date.append(i_element)
            
            data["check_in_date"] = "-".join(date)
            logger.debug("-".join(date))
            
        bot.send_message(message.from_user.id, "Я запомнил. Теперь введите дату выезда (гггг.мм.дд).")
        bot.set_state(message.from_user.id, HotelInfoState.check_out_date, message.chat.id)
        
    except TypeError:
        logger.debug(message.text.split("."))
        logger.warning("Invalid check in date.")
        bot.send_message(message.from_user.id, "Попробуйте еще раз.")
    except ValueError:
        logger.warning("Check in date is not integer.")
        bot.send_message(message.from_user.id, "Попробуйте еще раз.")


@bot.message_handler(state=HotelInfoState.check_out_date)
@logger.catch()
def get_check_out_date(message: Message) -> None:
    """ Хендлер для состояния запроса даты выезда. """
    
    logger.info("Check out date state in collecting hotel info started.")
    save_message(message)
    
    try:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            if len(message.text.split(".")) != 3:
                raise TypeError("Invalid check out date.")
            date = list()
            for i_element in message.text.split("."):
                if not i_element.isdigit():
                    raise ValueError("Check out date is not integer.")
                date.append(i_element)
                
            data["check_out_date"] = "-".join(date)
            logger.debug(date)
            
        bot.send_message(message.from_user.id, "Я запомнил. Теперь введите количество взрослых.")
        bot.set_state(message.from_user.id, HotelInfoState.adults, message.chat.id)
    
    except TypeError:
        logger.warning("Invalid check out date.")
        bot.send_message(message.from_user.id, "Попробуйте еще раз.")
    except ValueError:
        logger.warning("Check out date is not integer.")
        bot.send_message(message.from_user.id, "Попробуйте еще раз.")


@bot.message_handler(state=HotelInfoState.adults)
@logger.catch()
def get_adults_amount(message: Message) -> None:
    """ Хендлер для состояния запроса кол-ва взрослых. """
    
    logger.info("Get amount of adults state in collecting hotel info started.")
    save_message(message)
    
    bot.send_message(message.from_user.id, "Я запомнил. Теперь введите количество детей.")
    bot.set_state(message.from_user.id, HotelInfoState.kids, message.chat.id)
    
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["adults"] = message.text


@bot.message_handler(state=HotelInfoState.kids)
@logger.catch()
def get_kids_amount(message: Message) -> None:
    """ Хендлер для состояния запроса кол-ва детей. """
    
    logger.info("Get amount of kids state in collecting hotel info started.")
    save_message(message)
    
    try:
        kids_amount = int(message.text)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["kids_amount"] = kids_amount
            
        if kids_amount == 0:
            bot.send_message(message.from_user.id, "Отлично! Теперь я могу подобрать Вам отель.\nВведите вашу команду поиска еще раз.")
            bot.set_state(message.from_user.id, HotelInfoState.ready, message.chat.id)
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                save_travelers_info(data)
            # if data["first_command"] == "low":
            #     low(message)
            # elif data["first_command"] == "high":
            #     high(message)
            # elif data["first_command"] == "custom":
            #     custom(message)
                
        else:
            bot.send_message(message.from_user.id, "Я запомнил. Теперь введи через пробел их возрасты.")
            bot.set_state(message.from_user.id, HotelInfoState.kids_age, message.chat.id)
        
    except ValueError:
        logger.warning("Kids amount is not integer.")
        bot.send_message(message.from_user.id, "Попробуйте еще раз.")


@bot.message_handler(state=HotelInfoState.kids_age)
@logger.catch()
def get_kids_ages(message: Message) -> None:
    """ Хендлер для состояния запроса возрастов детей. """
    
    first_message = None
    logger.info("Get kids ages state in collecting hotel info started.")
    save_message(message)
    
    try:
        kids_ages = message.text.split()
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            if int(data["kids_amount"]) != len(kids_ages):
                logger.debug(int(data["kids"]))
                raise ValueError("Amount of kids and amount of ages does not match.")
            
            data["kids"] = message.text
            save_travelers_info(data)
            
            bot.set_state(message.from_user.id, HotelInfoState.ready, message.chat.id)
            bot.send_message(message.from_user.id, "Отлично! Теперь я могу подобрать Вам отель.")
            first_message = data["first_message"]
            
        # if first_message == "low":
        #     low(message)
        # elif first_message == "high":
        #     high(message)
        # elif first_message == "custom":
        #     custom(message)
        
    except ValueError:
        bot.send_message(message.from_user.id, "Попробуйте еще раз.")
        