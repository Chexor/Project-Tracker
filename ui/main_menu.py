# ui/main_menu.py

from data.database import Database

class MainMenu:
    """
    Main menu interface for the Project Time Tracker application.
    """
    def __init__(self, database:Database):
        self.database = database
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

    def display(self):
        print(self.header)
        print()
        for option in self.options:
            print(option)

    def display_active_session(self):
        active_session = self.get_active_session()
        if active_session:
            print("Actieve werksessie:")
            print(active_session)
        else:
            print("Geen actieve werksessie.")

    #def get_active_session(self):

    def menu_selection(self):
        return input(f"Kies een optie (1-{len(self.options)}): ")

