# main.py

from environs import Env
from data.database import Database
from ui.user_interface import UserInterface


def main():

    # Initialize environment variables
    env = Env()
    env.read_env()
    print("Environment variables loaded.")

    # Initialize the database
    db = Database()
    print("Database initialized.")

    # Initialize and launch User Interface
    UI = UserInterface(db)
    UI.run()

if __name__ == "__main__":
    main()



