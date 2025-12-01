# Project Tracker

CLI-applicatie om gepresteerde werkuren bij te houden voor verschillende projecten.

## Omschrijving
Deze applicatie stelt gebruikers in staat om hun werkuren per project bij te houden, rapporten te genereren en een overzicht te krijgen van de tijd die aan elk project is besteed.

## Functies
- **Projecten beheren**: Voeg nieuwe projecten toe, bewerk bestaande projecten en verwijder.
- **Uren registreren**: Log gepresteerde werkuren per project met beschrijvingen.
- **Rapporten genereren**: Genereer rapporten over de gepresteerde uren per project.

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


## Gebruik
1. Start de applicatie met het volgende commando:
```bash
python main.py
```
2. Navigeer door de menu-opties om projecten te beheren en uren te registreren.

## Vereisten
- Python 3.12 of hoger
- Pakketten zoals vermeld in `requirements.txt`
- SQLite database (standaard, kan worden aangepast in `.env`)

