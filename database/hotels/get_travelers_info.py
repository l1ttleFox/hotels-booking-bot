""" Файл для получения информации о путешественниках из бд.
    Этот файл в субпакете hotels, а не в travelers,
    потому что используется во время получения списка отелей по id локации."""

import sqlite3
from loguru import logger
import os


@logger.catch()
def pull_traveler_info(user_id: str) -> dict:
    """ Функция достаёт из бд последнюю запись, которую сделал в таблицу
        с информацией о путешественниках человек с user_id. """
    
    travelers_data = dict()
    
    path = os.path.join(os.path.abspath("database/db_files"), "travelers.db")
    with sqlite3.connect(path) as travelers:
        cur = travelers.cursor()
        cur.execute(f"""SELECT location_id, check_in_date, check_out_date, adults, kids, kids_ages FROM travelers
        WHERE user_id == {user_id}
        ORDER BY id DESC;""")
        
        raw_data = cur.fetchone()
        travelers_data["location_id"] = raw_data[0]
        travelers_data["check_in_date"] = raw_data[1].split("-")
        travelers_data["check_out_date"] = raw_data[2].split("-")
        travelers_data["adults"] = raw_data[3]
        if raw_data[4]:
            travelers_data["kids"] = raw_data[4]
            travelers_data["kids_ages"] = raw_data[5]
            children = []
            for i_child in raw_data[5].split():
                children.append({"age": int(i_child)})
            travelers_data["rooms"] = [
                {
                    "adults": raw_data[3],
                    "children": children
                }
            ]
            logger.debug(travelers_data["rooms"])
            
        else:
            travelers_data["rooms"] = [{"adults": travelers_data["adults"]}]
            
    return travelers_data


if __name__ == "__main__":
    logger.debug(pull_traveler_info(732290864))