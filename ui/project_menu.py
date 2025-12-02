# ui/project_menu.py

from datetime import datetime
from models.project import Project
from models.work_session import WorkSession
from data.database import Database
import services.csv_export


class ProjectMenu:
    """
    Projectmenu voor één specifiek project.
    Beheert werksessies, bewerken, archiveren en exporteren.
    """

    def __init__(self, project: Project, db: Database):
        self.project = project
        self.db = db
        # Zorg dat de sessies altijd up-to-date zijn
        self.project.work_sessions = self.db.get_work_sessions_for_project(project.proj_id)

        self.options = [
            "1. Start nieuwe werksessie",
            "2. Stop actieve werksessie",
            "3. Toon alle werksessies",
            "4. Bewerk project",
            "5. Rapport exporteren (CSV)",
            "6. Project archiveren",
            "7. Terug naar hoofdmenu",
        ]

# ===*** Hoofdloop methode ***===

    def run(self):
        """Hoofdloop van het projectmenu. Blijft draaien tot het menu wordt verlaten."""
        while True:
            self._print_header()
            self._print_active_session_status()
            self._print_menu()

            choice = input("Kies een optie (1-7): ").strip()

            if choice == "1":
                self._start_session()
            elif choice == "2":
                self._stop_session()
            elif choice == "3":
                self._show_sessions()
            elif choice == "4":
                self._edit_project()
            elif choice == "5":
                services.csv_export.export_project_to_csv(self.project)
            elif choice == "6":
                self._archive_project()
            elif choice == "7":
                print("Terug naar hoofdmenu...\n")
                return  # ← Belangrijk: stopt dit menu en keert terug naar MainMenu
            else:
                print("Ongeldige keuze. Probeer opnieuw.\n")

            input("Druk op Enter om door te gaan...")  # Gebruiksvriendelijke pauze

    # ===*** Validatie methoden ***===
    def check_for_active_session(self) -> bool:
        """
        Controleert of er al een actieve sessie lopende is (over alle projecten).
        Er kan maar één actieve sessie tegelijk zijn.
        :return: True als er een actieve sessie is, anders False."""
        active = self.db.get_active_work_session()
        if active:
            check = True
            if active.project_id == self.project.proj_id:
                msg = "Er is al een actieve sessie voor dit project!"
            else:
                msg = f"Er is al een actieve sessie voor project ID {active.project_id}!"
        else:
            check = False

        if check:
            print(msg)
            print("Stop eerst de actieve sessie voordat je een nieuwe start.")

        return check

    # ===*** Hulpmethoden voor menu acties ***===

    def _print_header(self):
        """Print het header van het projectmenu met projectdetails."""
        archived_status = " [GEARCHIVEERD]" if self.project.archived else ""
        print(f"\n{'='*60}")
        print(f" PROJECT: {self.project.name}{archived_status}")
        print(f" ID: {self.project.proj_id}")
        if self.project.description:
            print(f" Omschrijving: {self.project.description}")
        print(f" Aantal sessies: {len(self.project.work_sessions)}")
        print(f"{'='*60}")

    def _print_active_session_status(self):
        """Print de status van de actieve werksessie, indien aanwezig."""
        active = next((s for s in self.project.work_sessions if s.is_active), None)
        if active:
            duur = datetime.now() - active.start_time
            uren, rest = divmod(duur.seconds, 3600)
            minuten, seconden = divmod(rest, 60)
            print(f" ACTIEVE SESSIE: Gestart om {active.start_time.strftime('%H:%M:%S')}")
            print(f"                 Huidige duur: {uren}u {minuten}m {seconden}s")
            if active.description:
                print(f"                 → {active.description}")
        else:
            print(" Geen actieve werksessie")
        print("-" * 60)

    def _print_menu(self):
        """Print de beschikbare opties in het projectmenu."""
        for opt in self.options:
            print(opt)
        print()

    # ===*** Actie methoden ***===

    def _start_session(self):
        """Start een nieuwe werksessie voor het project."""
        if not self.check_for_active_session(): # Controleer op lopende sessie
            desc = input("Beschrijving sessie (optioneel): ").strip()
            session = WorkSession(
                project_id=self.project.proj_id,
                start_time=datetime.now(),
                description=desc or None
            )
            self.db.add_work_session_to_db(session)
            self.project.work_sessions.append(session)
            print(f"Nieuwe sessie gestart om {session.start_time.strftime('%H:%M:%S')}")

    def _stop_session(self):
        """Stopt de actieve werksessie voor het project."""
        active = next((s for s in self.project.work_sessions if s.is_active), None)
        if not active:
            print("Geen actieve sessie om te stoppen.")
            return

        active.end_time = datetime.now()
        self.db.update_work_session_in_db(active)
        print(f"Sessie gestopt → Totale duur: {active.duration_str()}")

    def _show_sessions(self):
        """Toont alle werksessies voor het project in een lijst."""
        if not self.project.work_sessions:
            print("Nog geen werksessies geregistreerd.")
            return

        print(f"\nWerksessies voor '{self.project.name}':")
        print("-" * 80)
        print(f"{'Start':<19} {'Einde':<19} {'Duur':<12} Beschrijving")
        print("-" * 80)
        for s in sorted(self.project.work_sessions, key=lambda x: x.start_time, reverse=True):
            start = s.start_time.strftime("%d/%m/%Y %H:%M")
            end = s.end_time.strftime("%H:%M") if s.end_time else "Lopend"
            duur = s.duration_str() if s.end_time else "← lopend"
            desc = s.description or "-"
            print(f"{start}  {end:<19} {duur:<12} {desc}")
        print()

    def _edit_project(self):
        """Bewerkt de naam en omschrijving van het project."""
        print(f"Huidige naam: {self.project.name}")
        new_name = input("Nieuwe naam (leeg = behouden): ").strip()
        if new_name:
            self.project.name = new_name

        print(f"Huidige omschrijving: {self.project.description or 'leeg'}")
        new_desc = input("Nieuwe omschrijving (leeg = behouden): ").strip()
        if new_desc:
            self.project.description = new_desc

        self.db.update_project_in_db(self.project)
        print("Project bijgewerkt!")

    def _archive_project(self):
        """Archiveert het project na bevestiging."""
        if self.project.archived:
            print("Dit project is al gearchiveerd.")
            return

        confirm = input(f"Weet je zeker dat je '{self.project.name}' wil archiveren? (j/N): ").strip().lower()
        if confirm in ("j", "ja", "y", "yes"):
            self.db.archive_project(self.project.proj_id)
            self.project.archived = True
            print(f"Project '{self.project.name}' is gearchiveerd.")
            return  # Direct terug naar hoofdmenu
        else:
            print("Archivering geannuleerd.")
