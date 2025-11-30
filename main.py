# main.py

from data.database import Database
from data.db_handler import DatabaseHandler
from ui.ui_handler import UIHandler


def main():
    # Initialize the database
    db = Database()
    db_handler = DatabaseHandler(db)

    # Initialize the UI
    ui = UIHandler()

