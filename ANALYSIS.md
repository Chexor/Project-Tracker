# Project Tracker - Analyse en Samenvatting

## Overzicht

**Project Tracker** is een command-line interface (CLI) applicatie geschreven in Python voor het bijhouden van werkuren per project. De applicatie maakt gebruik van een SQLite database voor persistente opslag en biedt een intuïtieve menu-gestuurde interface.

---

## Applicatie Functies

### Hoofdfunctionaliteiten

| Functie | Beschrijving |
|---------|--------------|
| **Projectbeheer** | Aanmaken, bewerken en archiveren van projecten |
| **Werksessie Tracking** | Starten en stoppen van werksessies met tijdregistratie |
| **Rapportage** | Exporteren van werksessies naar CSV-bestanden |
| **Actieve Sessie Monitoring** | Real-time weergave van lopende werksessies |

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

---

## Code Architectuur

### Directory Structuur

```
Project-Tracker/
├── main.py              # Applicatie entry point
├── config.py            # Configuratie en environment variabelen
├── data/
│   ├── __init__.py
│   └── database.py      # SQLite database operaties
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

---

## Code Analyse per Module

### 1. `main.py` - Entry Point

**Functie**: Initialiseert de database en start het hoofdmenu.

```python
if __name__ == "__main__":
    db = Database()
    menu = MainMenu(db)
    menu.run()
```

**Observaties**:
- Eenvoudige en duidelijke entry point
- Database wordt direct geïnitialiseerd
- Geen error handling bij startup

---

### 2. `config.py` - Configuratie

**Functie**: Laadt configuratie uit environment variabelen.

**Configureerbare Opties**:
| Variabele | Standaardwaarde | Beschrijving |
|-----------|-----------------|--------------|
| `DB_PATH` | `db/project_tracker.db` | Pad naar SQLite database |
| `EXPORT_PATH` | `export` | Directory voor CSV exports |

**Observaties**:
- Gebruikt `environs` library voor environment parsing
- Fallback naar defaults als `.env` niet gevonden wordt
- Duidelijke foutmelding bij ontbrekende `.env`

---

### 3. `models/project.py` - Project Model

**Klasse**: `Project` (dataclass)

**Attributen**:
| Attribuut | Type | Beschrijving |
|-----------|------|--------------|
| `name` | `str` | Projectnaam (verplicht) |
| `description` | `str` | Beschrijving (optioneel) |
| `proj_id` | `Optional[int]` | Database ID |
| `archived` | `bool` | Archiveeringstatus |
| `work_sessions` | `List[WorkSession]` | Gekoppelde werksessies |

**Methoden**:
- `total_duration` - Berekent totale tijd van afgesloten sessies
- `active_session` - Retourneert actieve sessie indien aanwezig
- `rename(new_name)` - Hernoemt project met validatie
- `set_description(description)` - Wijzigt beschrijving
- `archive()` / `unarchive()` - Archiveringsbeheer
- `add_work_session(session)` - Voegt werksessie toe

**Observaties**:
- Goed gebruik van Python dataclasses
- Properties voor afgeleide waarden
- Duidelijke string representaties (`__str__`, `__repr__`)

---

### 4. `models/work_session.py` - WorkSession Model

**Klasse**: `WorkSession` (dataclass)

**Attributen**:
| Attribuut | Type | Beschrijving |
|-----------|------|--------------|
| `project_id` | `int` | Gekoppeld project ID |
| `start_time` | `datetime` | Starttijd sessie |
| `description` | `str` | Sessie beschrijving |
| `end_time` | `Optional[datetime]` | Eindtijd (None = actief) |
| `id` | `Optional[int]` | Database ID |

**Methoden**:
- `is_active` - Property die aangeeft of sessie lopend is
- `duration` - Berekent duur als timedelta
- `duration_str()` - Formatteert duur als leesbare string (bv. "2u 34m 12s")
- `end()` - Stopt de sessie

**Observaties**:
- Type hint fout: `duration` property retourneert `timedelta`, niet `datetime`
- Goede formatting voor tijdweergave

---

### 5. `data/database.py` - Database Layer

**Klasse**: `Database`

**Database Schema**:

```sql
-- Projects tabel
CREATE TABLE projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    archived INTEGER DEFAULT 0 CHECK (archived IN (0, 1))
);

-- Work Sessions tabel
CREATE TABLE work_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    start_time TEXT NOT NULL,
    end_time TEXT,
    description TEXT,
    FOREIGN KEY(project_id) REFERENCES projects(id) ON DELETE CASCADE
);
```

**CRUD Operaties**:
| Methode | Beschrijving |
|---------|--------------|
| `add_project_to_db()` | Nieuw project toevoegen |
| `update_project_in_db()` | Project bijwerken |
| `archive_project()` | Project archiveren |
| `get_active_projects()` | Niet-gearchiveerde projecten |
| `get_all_projects_including_archived()` | Alle projecten |
| `add_work_session_to_db()` | Werksessie toevoegen |
| `update_work_session_in_db()` | Werksessie bijwerken |
| `get_work_sessions_for_project()` | Sessies per project |
| `get_active_work_session()` | Huidige actieve sessie |

**Observaties**:
- Gebruikt `sqlite3.Row` voor dict-achtige toegang
- ISO 8601 format voor datetime opslag
- Foreign key met ON DELETE CASCADE
- Max 1 actieve sessie tegelijk (LIMIT 1 query)

---

### 6. `services/csv_export.py` - Export Service

**Functie**: `export_project_to_csv(project: Project) -> str`

**CSV Kolommen**:
- Project ID
- Projectnaam
- Starttijd
- Eindtijd
- Duur
- Beschrijving

**Observaties**:
- Automatische directory creatie
- Timestamp in bestandsnaam voor uniekheid
- Duidelijke foutafhandeling met RuntimeError

---

### 7. `ui/main_menu.py` - Hoofdmenu

**Klasse**: `MainMenu`

**Verantwoordelijkheden**:
- Tonen van actieve projecten
- Projectnavigatie en -creatie
- Stoppen van actieve sessies
- Applicatie afsluiten

**Observaties**:
- Oneindige loop met `while True`
- Actieve sessie status wordt na elke actie ververst
- `sys.exit(0)` voor clean afsluiting

---

### 8. `ui/project_menu.py` - Projectmenu

**Klasse**: `ProjectMenu`

**Verantwoordelijkheden**:
- Werksessie start/stop
- Sessie overzicht
- Project bewerking
- CSV export
- Archivering

**Observaties**:
- Sessies worden bij init geladen
- Bevestiging vereist voor archivering
- Real-time duurberekening voor actieve sessies

---

## Technische Analyse

### Gebruikte Technologieën

| Technologie | Gebruik |
|-------------|---------|
| **Python 3.12+** | Programmeertaal |
| **SQLite** | Database |
| **dataclasses** | Data modellering |
| **environs** | Environment variabelen |
| **csv** | Export functionaliteit |

### Design Patterns

1. **Repository Pattern** - `Database` klasse voor data toegang
2. **Dataclass Pattern** - `Project` en `WorkSession` models
3. **Menu Pattern** - `MainMenu` en `ProjectMenu` voor UI

### Sterke Punten

✅ Duidelijke scheiding van verantwoordelijkheden (MVC-achtig)  
✅ Goed gebruik van Python type hints  
✅ Dataclasses voor clean data modellering  
✅ Configureerbare paden via environment variabelen  
✅ Nederlandse documentatie en foutmeldingen  
✅ Goede string representaties voor debugging  

### Verbeterpunten

⚠️ **Ontbrekende requirements.txt** - README verwijst ernaar maar bestand bestaat niet  
⚠️ **Type hint fout** - `WorkSession.duration` retourneert `timedelta`, niet `datetime`  
⚠️ **Geen tests** - Geen unit tests of integration tests aanwezig  
⚠️ **Geen error handling** - Bij database initialisatie en file operaties  
⚠️ **Geen input validatie** - Minimale validatie van gebruikersinvoer  
⚠️ **Hardcoded strings** - UI teksten niet geïnternationaliseerd  

---

## Aanbevelingen

### Korte Termijn
1. **Voeg requirements.txt toe** met `environs` dependency
2. **Fix type hint** in `WorkSession.duration` naar `timedelta`
3. **Voeg basis error handling toe** bij database en file operaties

### Middellange Termijn
1. **Voeg unit tests toe** voor models en database operaties
2. **Implementeer input validatie** voor alle gebruikersinvoer
3. **Voeg logging toe** voor debugging en monitoring

### Lange Termijn
1. **Internationalisatie (i18n)** voor meertalige ondersteuning
2. **Web interface** als alternatief voor CLI
3. **Meerdere gelijktijdige sessies** per project ondersteunen

---

## Conclusie

Project Tracker is een goed gestructureerde CLI applicatie voor urenregistratie. De code volgt goede Python practices met duidelijke scheiding tussen data, logica en presentatie lagen. De applicatie is functioneel compleet voor het beoogde doel maar zou baat hebben bij tests, betere error handling en een requirements.txt bestand.

**Geschiktheid**: Ideaal voor persoonlijk gebruik of kleine teams die een eenvoudige, lokale urenregistratie nodig hebben zonder complexe setup.

---

*Analyse uitgevoerd op: December 2024*
