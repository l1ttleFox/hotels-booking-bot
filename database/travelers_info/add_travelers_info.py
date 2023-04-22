""" Файл для добавления собранной информации о путешественниках в бд. """

import sqlite3
from loguru import logger
import os


@logger.catch()
def save_travelers_info(travelers_info: dict) -> None:
    """ Функция для добавления собранной информации о путешественниках в бд. """
    
    path = os.path.join(os.path.abspath("database/db_files"), "travelers.db")
    with sqlite3.connect(path) as travelers:
        cur = travelers.cursor()
        if travelers_info.get("kids", 0):
            cur.execute(f"""INSERT INTO travelers (user_id, location_id, check_in_date, check_out_date, adults, kids, kids_ages)
             VALUES ({int(travelers_info["user_id"])},
                     {travelers_info["detail_location_id"]},
                     "{travelers_info["check_in_date"]}",
                     "{travelers_info["check_out_date"]}",
                     {int(travelers_info["adults"])},
                     {int(travelers_info["kids_amount"])},
                     "{travelers_info["kids"]}");""")
        
        else:
            cur.execute(f"""INSERT INTO travelers (user_id, location_id, check_in_date, check_out_date, adults)
             VALUES ({int(travelers_info["user_id"])},
                     {travelers_info["detail_location_id"]},
                     "{travelers_info["check_in_date"]}",
                     "{travelers_info["check_out_date"]}",
                     {int(travelers_info["adults"])});""")
        