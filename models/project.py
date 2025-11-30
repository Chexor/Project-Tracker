# models\project.py

from work_session import WorkSession
from data.database import Database
from _datetime import datetime

class Project:
    """
    Represents a project with a name, description, and associated work sessions.
    """
    def __init__(self, name:str, description:str, proj_id:int=None, archived:bool=False):
        self.name = name
        self.description = description
        self.work_sessions = []
        self.proj_id = proj_id
        self.archived = archived

    def rename(self, new_name:str):
        self.name = new_name

    def archive(self):
        self.archived = True

    def set_description(self, description:str):
        self.description = description

    def start_work_session(self, description:str="", start_time:datetime=datetime.now()):
        ws = WorkSession(start_time=start_time, project_id=self.proj_id, description=description)
        self.work_sessions.append(ws)
        return ws

    def get_id_from_db(self):


    def __str__(self):
        return f"Project: {self.name} (ID: {self.id})\nDescription: {self.description}\nArchived: {self.archived}\nWork Sessions: {len(self.work_sessions)}"