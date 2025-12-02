# models/project.py

from dataclasses import dataclass, field
from typing import List, Optional
from models.work_session import WorkSession


@dataclass
class Project:
    """
    Representeert een project met naam, beschrijving, werksessies en archiefstatus.
    Wordt gebruikt in combinatie met SQLite en een command-line interface.
    """
    name: str
    description: str = ""
    proj_id: Optional[int] = None
    archived: bool = False
    work_sessions: List[WorkSession] = field(default_factory=list)

    def __post_init__(self):
        """Zorgt dat work_sessions altijd een lege lijst is als None wordt meegegeven."""
        if self.work_sessions is None:
            self.work_sessions = []

    @property
    def is_archived(self) -> bool:
        """Maakt het lezen van archived consistenter."""
        return self.archived

    @property
    def total_duration(self) -> str:
        """Totale tijd van alle afgesloten sessies (als leesbare string)."""
        total_seconds = sum(
            (s.duration.total_seconds() for s in self.work_sessions if not s.is_active),
            0
        )
        hours, remainder = divmod(int(total_seconds), 3600)
        minutes, seconds = divmod(remainder, 60)
        parts = []
        if hours:
            parts.append(f"{hours}u")
        if minutes:
            parts.append(f"{minutes}m")
        if seconds or not parts:
            parts.append(f"{seconds}s")
        return " ".join(parts) if parts else "0s"

    @property
    def active_session(self) -> Optional[WorkSession]:
        """Retourneert de actieve sessie (indien aanwezig)."""
        return next((s for s in self.work_sessions if s.is_active), None)

    def rename(self, new_name: str) -> None:
        """Wijzigt de naam van het project."""
        if not new_name.strip():
            raise ValueError("Projectnaam mag niet leeg zijn.")
        self.name = new_name.strip()

    def set_description(self, description: str) -> None:
        """Wijzigt de beschrijving (leeg = geen beschrijving)."""
        self.description = description.strip() if description else ""

    def archive(self) -> None:
        """Markeert het project als gearchiveerd."""
        self.archived = True

    def unarchive(self) -> None:
        """Haalt het project uit het archief (indien nodig)."""
        self.archived = False

    def add_work_session(self, session: WorkSession) -> None:
        """Voegt een werksessie toe aan het project."""
        if session.project_id != self.proj_id:
            session.project_id = self.proj_id
        self.work_sessions.append(session)

    def __str__(self) -> str:
        """Aangepaste weergave voor lijsten en logs."""
        archived_mark = " [GEARCHIVEERD]" if self.archived else ""
        sessie_count = len(self.work_sessions)
        active = " (1 actief)" if self.active_session else ""
        return f"[{self.proj_id or '?'}] {self.name}{archived_mark} – {sessie_count} sessie(s){active}"

    def __repr__(self) -> str:
        """Technische representatie voor debugging."""
        return (f"Project(id={self.proj_id}, name='{self.name}', "
                f"archived={self.archived}, sessions={len(self.work_sessions)})")