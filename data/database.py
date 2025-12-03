# data/database.py

import sqlite3
from datetime import datetime
from typing import List, Optional
from config import DB_PATH

from models.project import Project
from models.work_session import WorkSession


class Database:
    """Creëert en beheert de SQLite database voor projecten en werksessies."""
    def __init__(self):
        self.connection = sqlite3.connect(DB_PATH)
        self.connection.row_factory = sqlite3.Row  # ← dict-achtige rows
        self.create_tables()

    def create_tables(self):
        """Maakt de benodigde tabellen aan als ze nog niet bestaan."""
        cursor = self.connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                archived INTEGER DEFAULT 0 CHECK (archived IN (0, 1))
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS work_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT,
                description TEXT,
                FOREIGN KEY(project_id) REFERENCES projects(id) ON DELETE CASCADE
            )
        ''')
        self.connection.commit()

    # === PROJECTS ===
    def add_project_to_db(self, project: Project):
        """Voegt een nieuw project toe aan de database."""
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO projects (name, description, archived) VALUES (?, ?, ?)",
                (project.name, project.description or "", 0)
            )
            project.proj_id = cursor.lastrowid
            self.connection.commit()
        except sqlite3.Error as e:
            print("Fout bij toevoegen project aan database:", e)

    def update_project_in_db(self, project: Project):
        """Wijzigt een bestaand project in de database."""
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "UPDATE projects SET name = ?, description = ?, archived = ? WHERE id = ?",
                (project.name, project.description or "", int(project.archived), project.proj_id)
            )
            self.connection.commit()
        except sqlite3.Error as e:
            print("Fout bij bijwerken project in database:", e)

    def archive_project(self, project_id: int):
        """Zet archived = 1 → project verdwijnt uit 'actieve' lijst"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("UPDATE projects SET archived = 1 WHERE id = ?", (project_id,))
            self.connection.commit()
        except sqlite3.Error as e:
            print("Fout bij archiveren project in database:", e)

    def get_active_projects(self) -> List[Project]:
        """Alleen niet-gearchiveerde projecten"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT id, name, description, archived FROM projects WHERE archived = 0")
            rows = cursor.fetchall()
            return [Project(
                proj_id=row["id"],
                name=row["name"],
                description=row["description"] or "",
                archived=bool(row["archived"])
            ) for row in rows]
        except sqlite3.Error as e:
            print("Fout bij ophalen actieve projecten uit database:", e)
            return []

    def get_all_projects_including_archived(self) -> List[Project]:
        try:
            """Voor rapporten of admin-doelen"""
            cursor = self.connection.cursor()
            cursor.execute("SELECT id, name, description, archived FROM projects")
            rows = cursor.fetchall()
            return [Project(
                proj_id=row["id"],
                name=row["name"],
                description=row["description"] or "",
                archived=bool(row["archived"])
            ) for row in rows]
        except sqlite3.Error as e:
            print("Fout bij ophalen projecten uit database:", e)
            return []

    # === WORK SESSIONS ===
    def add_work_session_to_db(self, session: WorkSession):
        """Voegt een nieuwe werksessie toe aan de database."""
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                """INSERT INTO work_sessions 
                   (project_id, start_time, end_time, description) 
                   VALUES (?, ?, ?, ?)""",
                (
                    session.project_id,
                    session.start_time.isoformat(),
                    session.end_time.isoformat() if session.end_time else None,
                    session.description or ""
                )
            )
            session.id = cursor.lastrowid
            self.connection.commit()
        except sqlite3.Error as e:
            print("Fout bij toevoegen werksessie aan database:", e)

    def update_work_session_in_db(self, session: WorkSession):
        """Wijzigt een bestaande werksessie in de database."""
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                """UPDATE work_sessions 
                   SET end_time = ?, description = ? 
                   WHERE id = ?""",
                (
                    session.end_time.isoformat() if session.end_time else None,
                    session.description or "",
                    session.id
                )
            )
            self.connection.commit()
        except sqlite3.Error as e:
            print("Fout bij bijwerken werksessie in database:", e)

    def get_work_sessions_for_project(self, project_id: int) -> List[WorkSession]:
        """Retourneert alle werksessies voor een specifiek project."""
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "SELECT id, project_id, start_time, end_time, description FROM work_sessions WHERE project_id = ?",
                (project_id,)
            )
            rows = cursor.fetchall()
            sessions = []
            for row in rows:
                ws = WorkSession(
                    project_id=row["project_id"],
                    start_time=datetime.fromisoformat(row["start_time"]),
                    description=row["description"] or "",
                    end_time=datetime.fromisoformat(row["end_time"]) if row["end_time"] else None,
                    id=row["id"]
                )
                sessions.append(ws)
            return sessions
        except sqlite3.Error as e:
            print("Fout bij ophalen werksessies uit database:", e)
            return []

    def get_active_work_session(self) -> Optional[WorkSession]:
        """Return één actieve sessie (max. 1 tegelijk toegestaan)"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT ws.id, ws.project_id, ws.start_time, ws.description, p.name as project_name
                FROM work_sessions ws
                JOIN projects p ON ws.project_id = p.id
                WHERE ws.end_time IS NULL
                LIMIT 1
            """)
            row = cursor.fetchone()
            if row:
                return WorkSession(
                    project_id=row["project_id"],
                    start_time=datetime.fromisoformat(row["start_time"]),
                    description=row["description"],
                    id=row["id"]
                )
            return None
        except sqlite3.Error as e:
            print("Fout bij ophalen actieve werksessie uit database:", e)
            return None

    def close(self):
        self.connection.close()