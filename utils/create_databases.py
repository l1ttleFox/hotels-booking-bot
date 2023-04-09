""" Файл для создания бд для работы бота. """

import sqlite3
from loguru import logger
import os


# создание бд для хранения истории сообщений
path = os.path.join(os.path.abspath("database/db_files"), "history.db")
with sqlite3.connect(path) as hist:
    cur = hist.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS history (
    id INTEGER NOT NULL DEFAULT 1 PRIMARY KEY AUTOINCREMENT,
    message TEXT NOT NULL,
    chat_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    time DATETIME NOT NULL
    )""")
    logger.info("Message history database created.")
    

# создание бд для хранения информации об отелях
path = os.path.join(os.path.abspath("database/db_files"), "hotels.db")
with sqlite3.connect(path) as hotel:
    cur = hotel.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS hotels (
    id INTEGER NOT NULL DEFAULT 1 PRIMARY KEY AUTOINCREMENT,
    location_id INTEGER NOT NULL,
    hotel_id INTEGER NOT NULL,
    hotel_name TEXT NOT NULL,
    price TEXT NOT NULL,
    image TEXT
    )""")
    logger.info("Hotel info database created.")
    

# создание бд для хранения информации о путешественниках
path = os.path.join(os.path.abspath("database/db_files"), "travelers.db")
with sqlite3.connect(path) as hotel:
    cur = hotel.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS travelers (
    id INTEGER NOT NULL DEFAULT 1 PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    location_id INTEGER NOT NULL,
    check_in_date DATE NOT NULL,
    check_out_date DATE NOT NULL,
    adults INTEGER NOT NULL,
    kids INTEGER DEFAULT 0,
    kids_ages TEXT DEFAULT 0
    )""")
    logger.info("Travelers info database created.")
    