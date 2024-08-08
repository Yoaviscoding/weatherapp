import sqlite3
import os

class Database:
    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app', 'weather_data.db')
        self.db_connection = sqlite3.connect(self.db_path, check_same_thread=False)

    def create_table(self):
        cursor = self.db_connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS weather_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                localtime TEXT,
                name TEXT,
                country TEXT,
                temp_c REAL,
                condition_text TEXT
            )
        ''')
        self.db_connection.commit()

    def save_to_db(self, data):
        cursor = self.db_connection.cursor()
        cursor.execute('''
            INSERT INTO weather_data (localtime, name, country, temp_c, condition_text)
            VALUES (?, ?, ?, ?, ?)
        ''', (data['localtime'], data['name'], data['country'], data['temp_c'], data['condition_text']))
        self.db_connection.commit()

    def close_connection(self):
        self.db_connection.close()