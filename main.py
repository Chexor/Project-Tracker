# main.py
from environs import Env
from data.database import Database
import ui.user_interface as user_interface


def main():

    # Initialize the database
    db = Database()
    print("Database initialized.")

    # Load active projects
    active_projects = db.get_projects_from_db()


    # Launch UI
    user_interface.launch_ui(db)



if __name__ == "__main__":
    main()



