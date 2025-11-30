# models\project.py

from dataclasses import dataclass
from models.work_session import WorkSession
from _datetime import datetime

@dataclass
class Project:
    """
    Represents a project with a name, description, and associated work sessions.
    """
    name: str
    description: str
    work_sessions: list[WorkSession]
    proj_id: int = None
    archived: bool = False

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

    def __str__(self):
        return f"Project: {self.name} (ID: {self.id})\nDescription: {self.description}\nArchived: {self.archived}\nWork Sessions: {len(self.work_sessions)}"