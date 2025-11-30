# ui/user_interface.py

import sys

from models.project import Project
from models.work_session import WorkSession
from data.database import Database
from ui.main_menu import MainMenu

class UserInterface:
    """
    Command-line user interface voor de applicatie.
    Centrale klasse die alle interactie met de gebruiker afhandelt.
    """

    def __init__(self, db: Database):
        self.db = db
        self.menu = MainMenu()
        self.active_projects = []
        self.active_session: WorkSession | None = self.db.get_active_work_session_from_db()

    def run(self):
        while True:
            self.menu.show(active_session=self.active_session)

            selection = input(f"Selecteer een optie (1-{len(self.menu.options)}): ").strip()

            if selection == '1':
                # Toon actieve projecten
                self._show_active_projects()
            elif selection == '2':
                # Maak nieuw project
                self._new_project()
            elif selection == '3':
                # Start nieuwe werksessie
                self._start_new_session()
            elif selection == '4':
                # Beëindig actieve werksessie
                self._stop_active_session()
            elif selection == '5':
                # Exporteer CSV
                print("CSV exporteren... (nog te implementeren)")
            elif selection == '6':
                # Sluit project af
                print("Project afsluiten... (nog te implementeren)")
            elif selection == '7':
                # Afsluiten
                print("Afsluiten...")
                sys.exit(0)
            else:
                print("Ongeldige selectie. Probeer het opnieuw.")

# ------------
#  Functions
# ------------
    def _new_project(self):
        name = input("Voer naam van het nieuwe project in: ").strip()
        description = input("Voer een beschrijving in (optioneel): ").strip()
        new_project = Project(name=name, description=description)
        self.db.add_project_to_db(new_project)
        self.active_projects.append(new_project)

    def _show_active_projects(self):
        self.active_projects = self.db.get_projects_from_db()
        if not self.active_projects:
            print("Geen actieve projecten gevonden.\n")
            return
        else:
            print("Actieve projecten:")
            for project in self.active_projects:
                print(project)
        print()

    def _start_new_session(self):
        if self.active_session:
            print("Er is al een actieve werksessie. Beëindig deze eerst.")
            return

        self._show_active_projects()
        try:
            proj_id = int(input("Voer het ID van het project in om een werksessie te starten: ").strip())
        except ValueError:
            print("Ongeldig project ID.")
            return

        description = input("Voer een beschrijving in voor de werksessie (optioneel): ").strip() or None
        session = WorkSession(project_id=proj_id, description=description)
        self.db.add_work_session_to_db(session)
        self.active_session = session
        print(f"Werk sessie gestart voor project ID {proj_id}.")

    def _stop_active_session(self):
        if not self.active_session:
            print("Geen lopende werksessie om te beëindigen.")
            return
        self.active_session.end()
        self.db.update_work_session_in_db(self.active_session)
        self.active_session = None
        print(f"Werk sessie beëindigd: {self.active_session}")

    def _archive_project(self):
        self._show_active_projects()
        try:
            proj_id = int(input("Voer het ID van het project in om af te sluiten: ").strip())
        except ValueError:
            print("Ongeldig project ID.")
            return

        project_to_archive = next((p for p in self.active_projects if p.proj_id == proj_id), None)
        if not project_to_archive:
            print(f"Project met ID {proj_id} niet gevonden.")
            return

        project_to_archive.archive()
        self.db.update_project_in_db(project_to_archive)
        print(f"Project afgesloten: {project_to_archive}")
