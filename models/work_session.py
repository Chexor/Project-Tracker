# models/work_session.py

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional


@dataclass
class WorkSession:
    """
    Representeert een werksessie met start- en eindtijd, beschrijving en project-ID.
    Bevat methoden om de status en duur van de sessie te bepalen.
    """
    project_id: int
    start_time: datetime
    description: str = ""
    end_time: Optional[datetime] = None
    id: Optional[int] = None

    @property
    def is_active(self) -> bool:
        """Retourneert True als de sessie nog actief is (geen eindtijd)."""
        return self.end_time is None

    @property
    def duration(self) -> timedelta:
        """Retourneert de duur van de sessie als timedelta."""
        end = self.end_time or datetime.now()
        return end - self.start_time

    def duration_str(self) -> str:
        """
        Geeft een leesbare string terug van de duur.
        Bijv: "2u 34m 12s" of "45m 8s" of "1u 5m"
        """
        total_seconds = int(self.duration.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        parts = []
        if hours:
            parts.append(f"{hours}u")
        if minutes:
            parts.append(f"{minutes}m")
        if seconds or not parts:  # toon seconden als enige of als 0
            parts.append(f"{seconds}s")

        return " ".join(parts)

    def end(self) -> None:
        """Stop de sessie door end_time in te stellen."""
        if self.is_active:
            self.end_time = datetime.now()

    def __str__(self) -> str:
        """Aangepaste weergave voor lijsten en logs."""
        status = "LOPEND" if self.is_active else "AFGESLOTEN"
        duur = self.duration_str() if not self.is_active else f"{self.duration_str()} (lopend)"
        desc = f" – {self.description}" if self.description else ""
        return f"[{status}] {self.start_time.strftime('%d/%m %H:%M')} → {duur}{desc}"

    def __repr__(self) -> str:
        """Technische representatie voor debugging."""
        return (f"WorkSession(id={self.id}, project_id={self.project_id}, "
                f"start={self.start_time.isoformat()}, active={self.is_active})")