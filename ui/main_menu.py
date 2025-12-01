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
        Runs the main menu in a loop until exit.
        """
        self.active_session = active_session  # Store it
        while True:
            print(self.header)

            print("-" * len(self.header))
            if self.active_session:
                print(f"*** Actieve sessie: {self.active_session} ***")
            else:
                print("*** Geen actieve werksessie ***")
            print("-" * len(self.header))

            for option in self.options:
                print(option)
            print()

            selection = input(f"Selecteer een optie (1-{len(self.options)}): ").strip()

            if selection == '1':
                self._show_active_projects()
            elif selection == '2':
                self._open_project()
            elif selection == '3':
                new_proj = self._new_project()
                self._open_project(project=new_proj)
            elif selection == '4':
                #self._stop_active_session()
                print("Feature not implemented yet.")
            elif selection == '5':
                print("Exit...")
                sys.exit(0)
            else:
                print("Ongeldige selectie. Probeer het opnieuw.")

    def _show_active_projects(self):
        self.projects = self.db.get_projects_from_db()
        print()
        if not self.projects:
            print("Geen actieve projecten gevonden.\n")
            return
        else:
            print("Actieve projecten:")
            for project in self.projects:
                print(project)

    def _open_project(self, project: Project=None):
        if not project:
            self._show_active_projects()
            project_id_str = input("Voer de ID van het te openen project in: ").strip()
            if not project_id_str.isdigit():
                print("Ongeldige project ID. Probeer het opnieuw.")
                return
            else:
                project_id = int(project_id_str)
                selected_project = next((p for p in self.projects if p.proj_id == project_id), None)
                if selected_project:
                    project_menu = ProjectMenu(selected_project, self.db)
                    project_menu.run()
                else:
                    print("Project niet gevonden. Probeer het opnieuw.")
        else:
            project_menu = ProjectMenu(project, self.db)
            project_menu.run()

    def _new_project(self) -> Project:
        name = input("Voer naam van het nieuwe project in: ").strip()
        description = input("Voer een beschrijving in (optioneel): ").strip()
        new_project = Project(name=name, description=description)
        self.db.add_project_to_db(new_project)
        self.projects.append(new_project)
        return new_project