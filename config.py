from environs import Env

env = Env()
try:
    env.read_env('.env')
except FileNotFoundError as e:
    print(f"Waarschuwing: .env bestand niet gevonden. (Fallback to default)({e})")

DB_PATH = env.str("DB_PATH", "db/project_tracker.db")
EXPORT_PATH = env.str("EXPORT_PATH", "export")