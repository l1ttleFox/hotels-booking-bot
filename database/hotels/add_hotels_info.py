""" Файл для функции сохранения информации об отеле в бд. """

import sqlite3
from loguru import logger
import os


@logger.catch()
def save_hotel_info(hotels: dict) -> None:
    """ Функция сохраняет в бд информацию об отелях. """
    
    path = os.path.join(os.path.abspath("database/db_files"), "hotels.db")
    with sqlite3.connect(path) as hotel:
        cur = hotel.cursor()
        data = hotels["data"]
        property_search = data["propertySearch"]
        properties = property_search["properties"]
        
        for i_hotel in properties:
            location_id = i_hotel["destinationInfo"]["regionId"]
            hotel_id = i_hotel["id"]
            hotel_name = i_hotel["name"]
            price = i_hotel["price"]["displayMessages"][1]["lineItems"][0]["value"]
            image = i_hotel["propertyImage"]["image"]["url"]
            
            cur.execute(f"""INSERT INTO hotels (location_id, hotel_id, hotel_name, price, image) VALUES ({int(location_id)}, {hotel_id}, "{hotel_name}", "{price}", "{image}");""")
