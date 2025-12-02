# main.py
from data.database import Database
from ui.main_menu import MainMenu

if __name__ == "__main__":

    # Initialiseer de database
    db = Database()

    # Start het hoofdmenu
    menu = MainMenu(db)
    menu.run()