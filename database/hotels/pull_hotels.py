""" Файл для вытягивания из бд списка отелей по id локации. """

import sqlite3
import os
from loguru import logger


@logger.catch()
def pull_hotels(location_id: str | int) -> list:
    """ Функция достаёт из бд все отели, соответствующие location_id. """
    
    result_hotels = list()
    path = os.path.join(os.path.abspath("database/db_files"), "hotels.db")
    with sqlite3.connect(path) as hotels:
        cur = hotels.cursor()
        cur.execute(f"""SELECT hotel_id, hotel_name, price, image FROM hotels
                        WHERE location_id == {str(location_id)}
                        ORDER BY id DESC""")
        raw_hotels = cur.fetchall()
        
        for i_hotel in raw_hotels:
            logger.debug(i_hotel)
            
            if len(i_hotel) == 4:
                result_hotels.append(i_hotel)
            else:
                result_hotels.append((i_hotel[0], i_hotel[1], i_hotel[2], None))

    return result_hotels
