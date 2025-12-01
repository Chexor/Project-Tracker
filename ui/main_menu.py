# ui/main_menu.py

import sys
from data.database import Database
from ui.project_menu import ProjectMenu
from models.work_session import WorkSession
from models.project import Project


class MainMenu:
    """
    Hoofdmenu van de Project Time Tracker applicatie.
    Toont alleen actieve (niet-gearchiveerde) projecten en huidige actieve werksessie.
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

    def run(self):
        """Hoofdloop van de applicatie – blijft draaien tot afsluiten."""
        active_session = self.db.get_active_work_session()

        while True:
            self._print_header_and_status(active_session)
            self._print_options()

            choice = input("Selecteer een optie (1-5): ").strip()

            if choice == "1":
                self._show_active_projects()
            elif choice == "2":
                self._open_existing_project()
            elif choice == "3":
                new_project = self._create_new_project()
                if new_project:
                    self._open_project(new_project)
            elif choice == "4":
                self._stop_active_session()
                active_session = None  # Sessie is gestopt
            elif choice == "5":
                print("Tot ziens!")
                sys.exit(0)
            else:
                print("Ongeldige keuze. Probeer opnieuw.\n")

            # Na elke actie: check opnieuw of er een actieve sessie is
            active_session = self.db.get_active_work_session()
            input("Druk op Enter om door te gaan...")  # Kleine pauze voor leesbaarheid

    def _print_header_and_status(self, active_session: WorkSession | None):
        """Print het hoofdmenu header en de status van de actieve werksessie."""
        print(self.header)
        print("-" * 50)

        if active_session:
            project = next((p for p in self.db.get_active_projects()
                           if p.proj_id == active_session.project_id), None)
            proj_name = project.name if project else "Onbekend project"
            print(f"*** ACTIEVE SESSIE: {proj_name} ***")
            print(f"    Gestart om: {active_session.start_time.strftime('%H:%M:%S')}")
            if active_session.description:
                print(f"    Beschrijving: {active_session.description}")
        else:
            print("*** Geen actieve werksessie ***")

        print("-" * 50)

    def _print_options(self):
        """Print de beschikbare opties in het hoofdmenu."""
        for option in self.options:
            print(option)
        print()

    def _show_active_projects(self):
        print("\nActieve projecten:")
        print("-" * 50)
        projects = self.db.get_active_projects()
        if not projects:
            print("  → Nog geen projecten aangemaakt.")
        else:
            for p in projects:
                sessie_count = len(self.db.get_work_sessions_for_project(p.proj_id))
                print(f"  [{p.proj_id}] {p.name} – {sessie_count} sessie(s)"
                      f"{' (gearchiveerd)' if p.archived else ''}")
        print()

    def _open_existing_project(self):
        """Opent een bestaand project."""
        projects = self.db.get_active_projects()
        if not projects:
            print("Geen actieve projecten om te openen.")
            return

        self._show_active_projects()
        try:
            proj_id = int(input("Voer project-ID in: ").strip())
            project = next((p for p in projects if p.proj_id == proj_id), None)
            if project:
                project.work_sessions = self.db.get_work_sessions_for_project(project.proj_id)
                self._open_project(project)
            else:
                print("Project niet gevonden.")
        except ValueError:
            print("Ongeldige invoer. Voer een nummer in.")

    def _create_new_project(self):
        """Maakt een nieuw project aan."""
        print("\nNieuw project aanmaken")
        print("-" * 30)
        name = input("Naam van het project: ").strip()
        if not name:
            print("Naam is verplicht!")
            return None

        description = input("Beschrijving (optioneel): ").strip()

        project = Project(name=name, description=description)
        self.db.add_project_to_db(project)
        print(f"Project '{name}' aangemaakt met ID {project.proj_id}.")
        return project

    def _open_project(self, project):
        """Opent het projectmenu voor een specifiek project"""
        project.work_sessions = self.db.get_work_sessions_for_project(project.proj_id)
        project_menu = ProjectMenu(project, self.db)
        project_menu.run()

    def _stop_active_session(self):
        """Stopt de huidige actieve werksessie, indien aanwezig."""
        active = self.db.get_active_work_session()
        if not active:
            print("Er loopt geen actieve sessie.")
            return

        # Stop de sessie
        from datetime import datetime
        active.end_time = datetime.now()
        self.db.update_work_session_in_db(active)

        duur = active.duration_str()
        print(f"Sessie gestopt! Totale duur: {duur}")