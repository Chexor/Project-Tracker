# data/database.py

import sqlite3
import config.config as config

class Database:
    def __init__(self, db_name=config.DB_PATH):
        self.connection = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        cursor = self.connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS work_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER,
                start_time TEXT,
                end_time TEXT,
                FOREIGN KEY(project_id) REFERENCES projects(id)
            )
        ''')
        self.connection.commit()
        self.close()

    def connect(self):
        return self.connection

    def close(self):
        self.connection.close()

    def commit(self):
        self.connection.commit()


