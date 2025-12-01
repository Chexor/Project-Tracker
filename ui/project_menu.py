# ui/project_menu.py

import sys
from datetime import datetime
from models.project import Project
from models.work_session import WorkSession
from data.database import Database  # Nodig om project te updaten/verwijderen


class ProjectMenu:
    """
    Projectmenu voor een specifiek project.
    Beheert werksessies, bewerken, afsluiten en rapporten.
    """

    def __init__(self, project: Project, db: Database):
        self.project = project
        self.db = db  # Nodig voor opslaan/wissen
        self.sessions = project.work_sessions

        self.options = [
            "1. Start nieuwe werksessie",
            "2. Stop actieve werksessie",
            "3. Toon alle werksessies",
            "4. Bewerk project",
            "5. Project afsluiten (verwijderen)",
            "6. Rapport exporteren (CSV)",
            "7. Terug naar hoofdmenu",
        ]

    def run(self):
        while True:
            print("")
            self._print_header()
            self._print_active_session_status()
            self._print_options()

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
                if self._confirm("Weet je zeker dat je dit project wil verwijderen? (j/N): "):
                    self.db.delete_project(self.project.proj_id)
                    print(f"Project '{self.project.name}' verwijderd.")
                    return  # Terug naar hoofdmenu
            elif choice == "6":
                self._export_report()
            elif choice == "7":
                print("Terug naar hoofdmenu...")
                return  # Belangrijk: stopt ProjectMenu en keert terug naar MainMenu
            else:
                print("Ongeldige keuze. Probeer opnieuw.")

    def _print_header(self):
        header = f"""
\n=== Project: {self.project.name} (ID: {self.project.proj_id}) ===
Omschrijving: {self.project.description or 'Geen omschrijving'}
Aantal sessies: {len(self.sessions)}
        """
        print(header.strip())
        print("-" * 60)

    def _print_active_session_status(self):
        active = self._get_active_session()
        if active:
            duur = " (lopend)" if active.end_time is None else f" ({active.duration_str()})"
            print(f"*** Actieve sessie: {active.start_time.strftime('%H:%M')} - {active.description or 'Geen beschrijving'}{duur} ***")
        else:
            print("*** Geen actieve werksessie ***")
        print("-" * 60)

    def _print_options(self):
        for opt in self.options:
            print(opt)
        print()

    def _get_active_session(self) -> WorkSession | None:
        for session in self.sessions:
            if session.is_active:
                return session
        return None

    def _start_session(self):
        if self._get_active_session():
            print("Er loopt al een sessie! Stop die eerst.")
            return

        description = input("Beschrijving van de sessie (optioneel): ").strip()
        session = WorkSession(
            project_id=self.project.proj_id,
            start_time=datetime.now(),
            description=description
        )
        self.db.add_work_session_to_db(session)          # Opslaan in DB
        self.project.work_sessions.append(session)  # Ook in object houden
        print(f"Nieuwe sessie gestart om {session.start_time.strftime('%H:%M:%S')}")

    def _stop_session(self):
        active = self._get_active_session()
        if not active:
            print("Geen actieve sessie om te stoppen.")
            return

        active.end_time = datetime.now()
        self.db.update_work_session(active)  # Update in DB
        print(f"Sessie gestopt. Totale duur: {active.duration_str()}")

    def _show_sessions(self):
        if not self.sessions:
            print("Nog geen werksessies voor dit project.")
            return

        print("\nGeregistreerde werksessies:")
        print("-" * 60)
        for s in sorted(self.sessions, key=lambda x: x.start_time, reverse=True):
            status = "LOPEND" if s.is_active else s.duration_str()
            print(f"{s.start_time.strftime('%d/%m/%Y %H:%M')} → {status.ljust(12)} | {s.description or '-'}")
        print()

    def _edit_project(self):
        print(f"Huidige naam: {self.project.name}")
        new_name = input("Nieuwe naam (leeg = behouden): ").strip()
        if new_name:
            self.project.name = new_name

        print(f"Huidige omschrijving: {self.project.description or 'leeg'}")
        new_desc = input("Nieuwe omschrijving (leeg = behouden): ").strip()
        if new_desc:
            self.project.description = new_desc

        self.db.update_project(self.project)
        print("Project bijgewerkt.")

    def _export_report(self):
        # Optioneel: later implementeren met pandas of csv module
        print("Rapport exporteren (CSV) → nog niet geïmplementeerd.")
        print("Tip: Gebruik pandas.DataFrame(self.project.work_sessions).to_csv(...)")

    def _confirm(self, vraag: str) -> bool:
        antwoord = input(vraag).strip().lower()
        return antwoord in ("j", "ja", "y", "yes")