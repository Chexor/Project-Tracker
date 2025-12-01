# ui/main_menu.py

import sys
from data.database import Database
from models.project import Project
from ui.project_menu import ProjectMenu
from models.work_session import WorkSession


class MainMenu:
    """
    Main menu interface for the Project Time Tracker application.
    """
    def __init__(self, db: Database):
        self.db = db
        self.header = "\n=== Project Time Tracker ==="
        self.options = [
            "1. Toon actieve projecten",
            "2. Open project",
            "3. Maak nieuw project",
            "4. Stop actieve werksessie",
            "5. Afsluiten"
            ]
        self.projects = []
        self.active_session: WorkSession | None = None

    def run(self, active_session):
        """
        Toont header hoofd menu en de actieve werksessie indien aanwezig.
        + prompt voor selectie en voer de geselecteerde actie uit.
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

        self.prompt_selection_and_execute(active_session)

    def prompt_selection_and_execute(self, db: Database):
        while True:
            selection = input(f"Selecteer een optie (1-{len(self.options)}): ").strip()

            # Logic to handle the selection
            if selection == '1':
                # Toon actieve projecten
                self._show_active_projects(db)
            elif selection == '2':
                # Open project
                #self.open_project(db)
                print("Feature not implemented yet.")
            elif selection == '3':
                # Maak nieuw project
                new_proj = self._new_project(db)
                self._open_project(db, new_proj)
            elif selection == '4':
                # Stop actieve werksessie
                #self._stop_active_session(db)
                print("Feature not implemented yet.")
            elif selection == '5':
                # Afsluiten
                print("Exit...")
                sys.exit(0)
            else:
                print("Ongeldige selectie. Probeer het opnieuw.")

    def _show_active_projects(self, db: Database):
        self.active_projects = self.db.get_projects_from_db()
        print()
        if not self.active_projects:
            print("Geen actieve projecten gevonden.\n")
            return
        else:
            print("Actieve projecten:")
            for project in self.active_projects:
                print(project)

    def _open_project(self, db: Database, project: Project=None):
            if not project:
                self._show_active_projects(db)
                project = input("Voer de ID van het te openen project in: ").strip()
                if not project.isdigit():
                    print("Ongeldige project ID. Probeer het opnieuw.")
                else:
                    selected_project = next((p for p in self.active_projects if p.proj_id == int(project)), None)
                    if selected_project:
                        project_menu = ProjectMenu(selected_project)
                        project_menu.run()
                    else:
                        print("Project niet gevonden. Probeer het opnieuw.")
            else:
                project_menu = ProjectMenu(project)
                project_menu.run()

    def _new_project(self, db: Database) -> Project:
        name = input("Voer naam van het nieuwe project in: ").strip()
        description = input("Voer een beschrijving in (optioneel): ").strip()
        new_project = Project(name=name, description=description)
        self.db.add_project_to_db(new_project)
        self.active_projects.append(new_project)
        return new_project