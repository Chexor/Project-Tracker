# main.py

from data.database import Database
import ui.user_interface as UI

def main():

    # Initialize the database
    db = Database()
    db.create_tables()
    print("Database initialized.")

    # Launch UI
    UI.main(db)

if __name__ == "__main__":
    main()



