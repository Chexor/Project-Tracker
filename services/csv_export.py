# services/csv_export.py

import csv
import os
from datetime import datetime

from config import EXPORT_PATH
from models.project import Project

def export_project_to_csv(project: Project) -> str:
    """
    Exporteert alle werksessies van een project naar een CSV-bestand.
    Locatie van het bestand wordt bepaald door EXPORT_PATH in config.py.

    :param project: Het Project-object waarvan de sessies geëxporteerd moeten worden.
    :return: Het pad naar het geëxporteerde CSV-bestand.
    """
    # Zorg dat de export directory bestaat.
    os.makedirs(EXPORT_PATH, exist_ok=True)

    # Genereer bestandsnaam op basis van project ID en huidige datum/tijd.
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    file_name = f"project_{project.proj_id}_export_{timestamp}.csv"
    file_path = os.path.join(EXPORT_PATH, file_name)

    # Kolommen voor de CSV
    fieldnames = [
        "Project ID",
        "Projectnaam",
        "Starttijd",
        "Eindtijd",
        "Duur",
        "Beschrijving"
    ]

    # Schrijf de data naar het CSV-bestand.
    try:
        with open(file_path, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for session in project.work_sessions:
                writer.writerow({
                    "Project ID": project.proj_id,
                    "Projectnaam": project.name,
                    "Starttijd": session.start_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "Eindtijd": session.end_time.strftime("%Y-%m-%d %H:%M:%S") if session.end_time else "",
                    "Duur": session.duration_str() if not session.is_active else "Lopend",
                    "Beschrijving": session.description
                })
            print(f"Project '{project.name}' succesvol geëxporteerd naar {file_path}")
            return file_path

    except Exception as e:
        raise RuntimeError(f"Fout bij exporteren naar CSV: {e}")
