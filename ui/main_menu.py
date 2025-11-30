# ui/main_menu.py

from data.database import Database

class MainMenu:
    """
    Main menu interface for the Project Time Tracker application.
    """
    def __init__(self):
        self.header = "=== Project Time Tracker ==="
        self.options = [
            "1. Toon actieve projecten",
            "2. Maak nieuw project",
            "3. Start nieuwe werksessie",
            "4. Beëindig actieve werksessie",
            "5. Export CSV",
            "6. Afsluiten"
            ]
        self.projects = []

    def

