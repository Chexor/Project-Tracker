# ui/main_menu.py

from data.database import Database

class MainMenu:
    """
    Main menu interface for the Project Time Tracker application.
    """
    def __init__(self):
        self.header = "\n=== Project Time Tracker ==="
        self.options = [
            "1. Toon actieve projecten",
            "2. Maak nieuw project",
            "3. Start nieuwe werksessie",
            "4. Beëindig actieve werksessie",
            "5. Export CSV",
            "6. Sluit project af",
            "7. Afsluiten"
            ]
        self.projects = []

    def show(self, active_session):
        """
        Toont het hoofd menu (header en opties).
        + de actieve werksessie indien aanwezig.
        """
        print(self.header)

        print("-" * len(self.header))
        if active_session:
            print(f"*** Actieve sessie: {active_session} ***")
        else:
            print("*** Geen actieve werksessie ***")
        print("-" * len(self.header))

        for option in self.options:
            print(option)

        print()

