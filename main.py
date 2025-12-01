# main.py
from data.database import Database
from ui.main_menu import MainMenu

if __name__ == "__main__":
    db = Database()
    menu = MainMenu(db)
    menu.run()