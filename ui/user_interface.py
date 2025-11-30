# ui/user_interface.py

from ui.main_menu import MainMenu
from data.database import Database


class UserInterface:
    """
    User interface for the Project Time Tracker application.
    """
    def __init__(self, db: Database):
        self.db = db
        self.main_menu = MainMenu()
        self.active_projects = db.get_projects_from_db()
        self.active_session = db.get_active_work_session_from_db()

    def launch(self):
        while True:
            # Toon header
            print(self.main_menu.header)

            # Toon actieve werksessie
            if self.active_session:
                print(f"*** Actieve sessie: {self.active_session} ***")
            else:
                print("*** Geen actieve werksessie ***")

            # Toon menu-opties
            for option in self.main_menu.options:
                print(option)

            # Vraag om gebruikersinvoer
            selection = input(f"Selecteer een optie (1-{len(self.main_menu.options)}
                            
            # Verwerk gebruikersinvoer
            if selection == "1":
                self.show_active_projects()
            elif selection == "2":
                self.create_new_project()
            elif selection == "3":
                self.start_new_work_session()
            elif selection == "4":
                self.end_active_work_session()
            elif selection == "5":
                self.export_csv()
            elif selection == "6":
                print("Afsluiten...")
                break
            else:
                print("Ongeldige selectie. Probeer het opnieuw.")

    def show_active_projects(self):
        print("Actieve projecten:")
        for project in self.active_projects:
            print(project)

    def create_new_project(self):
        name = input("Voer de naam van het nieuwe project in: ")
        description = input("Voer een beschrijving in (optioneel): ")
        new_project = Project(name=name, description=description)
        self.db.add_project_to_db(new_project)
        self.active_projects.append(new_project)
        print(f"Project '{name}' aangemaakt.")

    def start_new_work_session(self):
        self.show_active_projects()
        proj_id = int(input("Voer het ID van het project in om een werksessie te starten: "))
        description = input("Voer een beschrijving in voor de werksessie (optioneel): ")
        project = next((p for p in self.active_projects if p.proj_id == proj_id), None)
        if project:
            new_session = project.start_work_session(description=description)
            self.db.add_work_session_to_db(new_session)
            self.active_session = new_session
            print(f"Werk sessie gestart voor project '{project.name}'.")
        else:
            print("Ongeldig project ID.")

    def end_active_work_session(self):
        if self.active_session:
            self.active_session.end()
            self.db.update_work_session_in_db(self.active_session)
            print(f"Werk sessie beëindigd: {self.active_session}")
            self.active_session = None
        else:
            print("Er is geen actieve werksessie om te beëindigen.")






