
import sqlite3
import Settings.config as config
from models.project import Project
from models.work_session import WorkSession
from datetime import datetime

class Database:
    def __init__(self):
        self.db = config.DB_PATH
        self.connection = sqlite3.connect(self.db)

    def create_tables(self):
        cursor = self.connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS work_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER,
                start_time TEXT,
                end_time TEXT,
                FOREIGN KEY(project_id) REFERENCES projects(id)
            )
        ''')
        self.connection.commit()

    def add_project_to_db(self, project: Project) -> int:
        """
        Adds a new project to the database.
        + Adds the project ID to the project instance.
        """
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO projects (name, description, archived) VALUES (?, ?, ?)",
            (project.name, project.description, int(project.archived))
        )
        self.connection.commit()
        project.proj_id = cursor.lastrowid

    def add_work_session_to_db(self, work_session: WorkSession):
        """
        Adds a new work session to the database.
        Args:
            work_session (WorkSession): The work session to add.
        Returns:
            None
        """
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO work_sessions (project_id, start_time, end_time, description) VALUES (?, ?, ?, ?)",
            (
                work_session.project_id,
                work_session.start_time.isoformat(),
                work_session.end_time.isoformat() if work_session.end_time else None,
                work_session.description
            )
        )

    def update_project_in_db(self, project: Project):
        cursor = self.connection.cursor()
        cursor.execute(
            "UPDATE projects SET name = ?, description = ?, archived = ? WHERE id = ?",
            (project.name, project.description, int(project.archived), project.proj_id)
        )
        self.connection.commit()

    def update_work_session_in_db(self, work_session: WorkSession):
        cursor = self.connection.cursor()
        cursor.execute(
            "UPDATE work_sessions SET start_time = ?, end_time = ?, description = ? WHERE id = ?",
            (
                work_session.start_time.isoformat(),
                work_session.end_time.isoformat() if work_session.end_time else None,
                work_session.description,
                work_session.id
            )
        )
        self.connection.commit()

    def get_projects_from_db(self) -> list[Project]:
        cursor = self.connection.cursor()
        cursor.execute("SELECT id, name, description, archived FROM projects")
        rows = cursor.fetchall()
        projects = []
        for row in rows:
            proj = Project(
                name=row[1],
                description=row[2],
                proj_id=row[0],
                archived=bool(row[3])
            )
            projects.append(proj)
        return projects

    def get_work_sessions_for_project_from_db(self, project:Project) -> list[WorkSession]:
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT id, start_time, end_time, description FROM work_sessions WHERE project_id = ?",
            (project.proj_id,)
        )
        rows = cursor.fetchall()
        work_sessions = []
        for row in rows:
            ws = WorkSession(
                start_time=datetime.fromisoformat(row[1]),
                project_id=project.proj_id,
                description=row[3],
                end_time=datetime.fromisoformat(row[2]) if row[2] else None,
                id=row[0]
            )
            work_sessions.append(ws)
        return work_sessions

    def get_active_work_session_from_db(self):
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT id, project_id, start_time, description FROM work_sessions WHERE end_time IS NULL"
        )
        row = cursor.fetchone()
        if row:
            ws = WorkSession(
                start_time=datetime.fromisoformat(row[2]),
                project_id=row[1],
                description=row[3],
                id=row[0]
            )
            return ws
        return None