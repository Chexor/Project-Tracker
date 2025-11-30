# models/work_session.py

from dataclasses import dataclass
from datetime import datetime

@dataclass
class WorkSession:
    project_id: int
    description: str = ""
    start_time: datetime = datetime.now()
    end_time: datetime = None
    id: int = None
    is_active: bool = True

    def __str__(self) -> str:
        return f"(Project:{self.project_id}, Description: {self.description}, Started: {self.start_time})"

    def end(self):
        self.is_active = False
        self.end_time = datetime.now()

    def change_description(self, new_description: str):
        self.description = new_description

    def change_project_id(self, new_project_id: int):
        self.project_id = new_project_id

    def change_start_time(self, new_start_time: datetime):
        self.start_time = new_start_time

    def change_end_time(self, new_end_time: datetime):
        self.end_time = new_end_time



