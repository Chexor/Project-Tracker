# main.py

from data.database import Database
from ui.user_interface import UserInterface


def main():

    # Initialize the database
    db = Database()
    print("Database initialized.")
    print("")

    # Initialize and launch User Interface
    UI = UserInterface(db)
    UI.run()

if __name__ == "__main__":
    main()



