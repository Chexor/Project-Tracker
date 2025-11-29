# models/work_session.py

from dataclasses import dataclass
from datetime import datetime

@dataclass
class WorkSession:
    start_time: datetime
    project_id: int
    description: str = ""
    end_time: datetime = None
    id: int = None

    def __str__(self) -> str:
        return f"WorkSession(ID: {self.id}, Start: {self.start_time}, End: {self.end_time}, Description: {self.description})"