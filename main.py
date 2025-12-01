# main.py

from data.database import Database
from ui.main_menu import MainMenu
from ui.user_interface import UserInterface


if __name__ == "__main__":

    # Initialize the database
    db = Database()
    print("Database initialized.")

    # Initialize and launch User Interface
    active_session = db.get_active_work_session_from_db()
    main_menu = MainMenu(db)
    main_menu.run(active_session=active_session)



