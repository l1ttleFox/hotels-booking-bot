import sqlite3
from loguru import logger


with sqlite3.connect("database/history.db") as hist:
    cur = hist.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS history(
    id INTEGER NOT NULL DEFAULT 1 PRIMARY KEY AUTOINCREMENT,
    message TEXT NOT NULL,
    chat_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    time DATETIME NOT NULL
    )""")
    logger.info("Message history database created.")