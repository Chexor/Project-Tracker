# ui/ui_handler.py

class UIHandler:
    """
    Handles user interface interactions for the Project Time Tracker application.
    """

from models.project import Project
from models.work_session import WorkSession
from ui.main_menu import MainMenu
import data.db_handler as db_handler

class ui_handler.py
    def __init__(self):
        self.main_menu = MainMenu()
        self.project_menu = ProjectMenu()
        self.projects = [Project]
        self.active_work_session = None

    def load_projects_from_db(self, db: db_handler.DatabaseHandler):
        self.projects = db.get_projects_from_db()


