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

        print(self.header)

    def show(self, active_session):
        """
        Toont het hoofd menu (header en opties).
        + de actieve werksessie indien aanwezig.
        """
        print(self.header)

        if active_session:
            print(f"*** Actieve sessie: {active_session} ***")
        else:
            print("*** Geen actieve werksessie ***")

        for option in self.options:
            print(option)

        print()

