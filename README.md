# Project Tracker

CLI-applicatie om gepresteerde werkuren bij te houden voor verschillende projecten.

## Omschrijving
**Project Tracker** is een command-line interface (CLI) applicatie geschreven in Python voor het bijhouden van werkuren per project.  
De applicatie maakt gebruik van een SQLite database voor persistente opslag en biedt een menu-gestuurde interface.


### Hoofdfunctionaliteiten

| Functie | Beschrijving |
|---------|--------------|
| **Projectbeheer** | Aanmaken, bewerken en archiveren van projecten |
| **Werksessie Tracking** | Starten en stoppen van werksessies met tijdregistratie |
| **Rapportage** | Exporteren van werksessies naar CSV-bestanden |
| **Actieve Sessie Monitoring** | Real-time weergave van lopende werksessies |

## Installatie
1. Maak en activeer een virtuele omgeving:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Voor Unix-systemen
   .venv\Scripts\activate.bat  # Voor Windows
   ```
2. Installeer de vereiste pakketten:
   ```bash
   pip install -r requirements.txt
   ```
3. Kopieer `.env.example` naar `.env` en pas de configuratie aan indien nodig.

## Database
De applicatie gebruikt een SQLite database voor het opslaan van projecten en werksessies.  
De database wordt automatisch aangemaakt in de default locatie bij de eerste uitvoering van de applicatie.  
De default locatie van de database 'database/project_tracker.db' kan worden aangepast via de `.env` configuratie.

## Gebruik
1. Start de applicatie met het volgende commando:
```bash
python main.py
```
2. Navigeer door de menu-opties om projecten te beheren en uren te registreren.


### Menu Structuur

```
Hoofdmenu (MainMenu)
├── 1. Toon actieve projecten
├── 2. Open project → Projectmenu (ProjectMenu)
│   ├── 1. Start nieuwe werksessie
│   ├── 2. Stop actieve werksessie
│   ├── 3. Toon alle werksessies
│   ├── 4. Bewerk project
│   ├── 5. Rapport exporteren (CSV)
│   ├── 6. Project archiveren
│   └── 7. Terug naar hoofdmenu
├── 3. Maak nieuw project
├── 4. Stop actieve werksessie
└── 5. Afsluiten
```

## Code Architectuur

### Directory Structuur

```
Project-Tracker/
├── main.py              # Applicatie entry point
├── config.py            # Configuratie en environment variabelen
├── data/
│   ├── __init__.py
│   └── database.py      # SQLite database operaties
├── database/            # Default locatie voor SQLite database
├── export/              # Default locatie voor geëxporteerde CSV-bestanden
├── models/
│   ├── __init__.py
│   ├── project.py       # Project dataclass
│   └── work_session.py  # WorkSession dataclass
├── services/
│   ├── __init__.py
│   └── csv_export.py    # CSV export functionaliteit
├── ui/
│   ├── __init__.py
│   ├── main_menu.py     # Hoofdmenu interface
│   └── project_menu.py  # Projectmenu interface
├── .env.example         # Voorbeeld configuratie
├── .gitignore           # Git ignore regels
└── README.md            # Documentatie
```

### Lagen Architectuur

De applicatie volgt een gelaagde architectuur:

```
┌─────────────────────────────────────┐
│           UI Layer (ui/)            │
│  MainMenu, ProjectMenu              │
├─────────────────────────────────────┤
│       Services Layer (services/)    │
│  csv_export                         │
├─────────────────────────────────────┤
│         Data Layer (data/)          │
│  Database                           │
├─────────────────────────────────────┤
│       Models Layer (models/)        │
│  Project, WorkSession               │
├─────────────────────────────────────┤
│         Configuration (config.py)   │
│  Environment variabelen             │
└─────────────────────────────────────┘
```


