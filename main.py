# main.py
import sqlite3
import sys
import os

from config import DB_PATH
from data.database import Database
from ui.main_menu import MainMenu

if __name__ == "__main__":

    try:
        # Controleer of de benodigde mappen bestaan, anders aanmaken
        os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)
        db = Database()
    except sqlite3.Error as e:
        print(f"Fout bij het initialiseren van de database: {e}")
        sys.exit(1)
    except PermissionError:
        print("Fout: Geen toestemming om de database te maken of te openen.")
        sys.exit(1)

    try:
        menu = MainMenu(db)
        menu.run()
    except KeyboardInterrupt:
        print("\nProgramma beëindigd door gebruiker.")
        sys.exit(0)
    finally:
        db.close()