# ui/user_interface.py
from ui.main_menu import MainMenu

def main(database):
    # Initialize and display the main menu
    main_menu = MainMenu(database)
    while True:
        main_menu.display()
        main_menu.display_active_session()
        choice = main_menu.menu_selection()
        if choice == '6':
            print("Exiting the application.")
            break
        # Here you would handle other menu options

if __name__ == "__main__":
    main()





