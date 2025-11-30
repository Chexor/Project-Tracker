# services/csv_export.py

import csv
from models.WorkSession import WorkSession
from models.Project import Project

def export_work_sessions_to_csv(project:Project, file_path: str) -> None:
    """
    Exporteer een lijst van WorkSession objecten naar een CSV-bestand.

    :param sessions: Lijst van WorkSession objecten die geëxporteerd moeten worden.
    :param file_path: Pad naar het CSV-bestand waar de gegevens opgeslagen moeten worden.
    """
    with open(file_path, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['id', 'project_id', 'description', 'start_time', 'end_time', 'is_active']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for session in sessions:
            writer.writerow({
                'id': session.id,
                'project_id': session.project_id,
                'description': session.description,
                'start_time': session.start_time,
                'end_time': session.end_time,
                'is_active': session.is_active
            })

