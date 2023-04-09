""" Файл для вытягивания из бд id локации по user_id. """

import sqlite3
import os
from loguru import logger


@logger.catch()
def pull_location_id(user_id: str) -> int:
    """ Функция для получения из бд location_id по user_id. """
    
    path = os.path.join(os.path.abspath("database//db_files"), "travelers.db")
    with sqlite3.connect(path) as travelers:
        cur = travelers.cursor()
        cur.execute(f"""SELECT location_id FROM travelers
                        WHERE user_id == {user_id}
                        ORDER BY id DESC""")
        
        location_id = int(cur.fetchone()[0])
        
    return location_id
        