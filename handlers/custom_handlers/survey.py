""" Файл для команды /survey. """

from loader import bot
from telebot.types import Message
from states.contact_info import UserInfoState
from keyboards.reply.contact import request_contact
from loguru import logger
from database.history.message_history import save_message


@bot.message_handler(commands=["survey"])
@logger.catch()
def survey(message: Message) -> None:
    """ Хендлер для начала опроса. """
    
    logger.info("Survey started.")
    save_message(message)
    
    bot.set_state(message.from_user.id, UserInfoState.name, message.chat.id)
    bot.send_message(message.from_user.id, f"Доброго дня, {message.from_user.username}. Введите Ваше имя")
    
    
@bot.message_handler(state=UserInfoState.name)
@logger.catch()
def get_name(message: Message) -> None:
    """ Хендлер для состояния запроса имени. """
    
    logger.info("Name state in survey started.")
    save_message(message)
    
    if message.text.isalpha():
        bot.send_message(message.from_user.id, "Я запомнил. Теперь введите Ваш возраст.")
        bot.set_state(message.from_user.id, UserInfoState.age, message.chat.id)
        
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["name"] = message.text
    else:
        bot.send_message(message.from_user.id, "Имя может содержать только буквы.")


@bot.message_handler(state=UserInfoState.age)
@logger.catch()
def get_age(message: Message) -> None:
    """ Хендлер для состояния запроса возраста. """
    
    logger.info("Age state in survey started.")
    save_message(message)
    
    if message.text.isdigit():
        bot.send_message(message.from_user.id, "Я запомнил. Теперь введите Вашу страну.")
        bot.set_state(message.from_user.id, UserInfoState.country)
        
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["age"] = message.text
    else:
        bot.send_message(message.from_user.id, "Возраст может содержать только цифры.")


@bot.message_handler(state=UserInfoState.country)
@logger.catch()
def get_country(message: Message) -> None:
    """ Хендлер для состояния запроса страны. """
    
    logger.info("Country state in survey started.")
    save_message(message)
    
    bot.send_message(message.from_user.id, "Я запомнил. Теперь введите Ваш город.")
    bot.set_state(message.from_user.id, UserInfoState.city, message.chat.id)
    
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["country"] = message.text


@bot.message_handler(state=UserInfoState.city)
@logger.catch()
def get_city(message: Message) -> None:
    """ Хендлер для состояния запроса города. """
    
    logger.info("City state in survey started.")
    save_message(message)
    
    bot.send_message(message.from_user.id, "Я запомнил. Теперь нажмите на кнопку, чтобы запустить самоуничтожение.")
    bot.send_message(message.from_user.id, "Шучу, конечно. Она отправит мне Ваш номер телефона",
                     reply_markup=request_contact())
    
    bot.set_state(message.from_user.id, UserInfoState.phone_number, message.chat.id)
    
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["city"] = message.text
        

@bot.message_handler(state=UserInfoState.phone_number, content_types=["contact"])
@logger.catch()
def get_phone_number(message: Message) -> None:
    """ Хендлер для состояния запроса номера телефона. """
    
    logger.info("Contact state in survey started.")
    save_message(message)
    
    if message.content_type == "contact":
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["phone_number"] = message.contact.phone_number
            
            total_info = "Имя: {name}\nВозраст: {age}\nСтрана: {country}\nГород: {city}\n Номер телефона: {phone_number}".format(
                name=data["name"],
                age=data["age"],
                country=data["country"],
                city=data["city"],
                phone_number=data["phone_number"]
            )

        bot.send_message(message.from_user.id, "Спасибо за ваши данные!")
        bot.send_message(message.from_user.id, "Если в данных есть ошибка, пройдите опрос заново.")
        bot.send_message(message.from_user.id, total_info)
        bot.delete_state(message.from_user, message.chat.id)
            
    else:
        bot.send_message(message.from_user.id, "Пожалуйста, нажмите на кнопку.")
        