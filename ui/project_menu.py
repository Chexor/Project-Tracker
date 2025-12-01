# ui/project_menu.py

from models.project import Project
from models.work_session import WorkSession

class ProjectMenu:
    """
    Project menu interface for managing projects.
    """
    def __init__(self, project:Project):

        self.project = project
        self.sessions = project.work_sessions
        self.active_session = None

        self.header = f"""
=== Project Menu: ID {project.proj_id} ===
Naam: {project.name}
Omschrijving: {project.description}
        """

        self.options = [
            "1. Toon geregistreerde werksessies",
            "2. Bewerk project",
            "3. Project afsluiten",
            "4. Rapport exporteren (CSV)",
            "5. Terug naar hoofdmenu"
        ]

    def run(self):
        """
        Toont het project menu (header en opties).
        """
        while True:
            print(self.header)

            print("-" * len(self.header))
            active_session = self.check_for_active_session()
            if active_session:
                print(f"*** Actieve sessie: {active_session} ***")
            else:
                print("*** Geen actieve werksessie ***")
            print("-" * len(self.header))

            for option in self.options:
                print(option)
            print()

    def check_for_active_session(self):
        """
        Controleer of er een actieve werksessie is voor dit project.
        """
        for session in self.sessions:
            if session.is_active:
                self.active_session = session
                return session
        return None
