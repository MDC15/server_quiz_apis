# database.py
import sqlite3
import logging
from datetime import datetime

logging.basicConfig(
    filename="quiz_app.log",
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s",
)


class Database:
    def __init__(self, db_name="players.db"):
        self.db_name = db_name
        self.create_tables()

    def get_connection(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn

    def create_tables(self):
        try:
            conn = self.get_connection()
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS players (
                    id_hash TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    score INTEGER NOT NULL,
                    time TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )
            conn.commit()
            logging.info("Database tables created successfully")
        except Exception as e:
            logging.error(f"Error creating tables: {str(e)}")
        finally:
            conn.close()
