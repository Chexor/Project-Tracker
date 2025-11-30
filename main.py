# main.py

from data.database import Database
from ui.main_menu import MainMenu

def main():

    # Initialize the database
    db = Database()
    db.create_tables()
    print("Database initialized.")

    # Launch UI
    main_menu = MainMenu()
    while True:
        main_menu.display_menu()
        choice = main_menu.prompt_for_menu_choice()
        main_menu.handle_menu_choice(choice)
        if choice == '6':
            break

if __name__ == "__main__":
    main()



