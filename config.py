from environs import Env

env = Env()
env.read_env()  # leest .env als die bestaat

DB_PATH = env.str("DB_PATH", default="db/project_tracker.db")