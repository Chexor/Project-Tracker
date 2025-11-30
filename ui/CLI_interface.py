# ui/CLI_interface.py

import data.database as db

from models.project import Project
from models.work_session import WorkSession
from CLI_interface.main_menu import MainMenu

class ui_handler.py
    def __init__(self):
        self.main_menu = MainMenu()
        self.projects = [Project]
        self.active_work_session = None

    def load_projects_from_db(self, db):
        self.projects = db.get_projects_from_db()


