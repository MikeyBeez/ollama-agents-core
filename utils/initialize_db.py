# ollama-agents-core/utils/initialize_db.py

import sqlite3
from pathlib import Path
import sys

# Add the ollama-agents-data directory to the Python path
ollama_agents_data_dir = Path.home() / "ollama-agents-data"
sys.path.insert(0, str(ollama_agents_data_dir))

print(f"Python path: {sys.path}")

# Now import from the config file in ollama-agents-data
from config import DB_FILE, EDGE_TABLE_NAME, DATA_DIR

print(f"DATA_DIR from config: {DATA_DIR}")

# Import the schema from ollama-agents-data
schema_path = DATA_DIR / "schema.py"
if not schema_path.exists():
    raise FileNotFoundError(f"Schema file not found at: {schema_path}")

print(f"Loading schema from: {schema_path}")
from schema import SCHEMA

print(f"DB_FILE: {DB_FILE}")
print(f"EDGE_TABLE_NAME: {EDGE_TABLE_NAME}")

def initialize_database():
    db_file = Path(DB_FILE).expanduser()
    db_dir = db_file.parent

    print(f"Initializing database at: {db_file}")
    print(f"Database directory: {db_dir}")

    # Ensure the database directory exists
    db_dir.mkdir(parents=True, exist_ok=True)
    print(f"Ensured database directory exists")

    if db_file.exists():
        print(f"Database file already exists")
        conn = sqlite3.connect(str(db_file))
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (EDGE_TABLE_NAME,))
        if cursor.fetchone():
            print(f"Main table '{EDGE_TABLE_NAME}' already exists")
            conn.close()
            return
        conn.close()

    print(f"Creating new database")
    conn = sqlite3.connect(str(db_file))
    cursor = conn.cursor()

    print(f"Executing schema")
    cursor.executescript(SCHEMA)

    print(f"Committing changes")
    conn.commit()
    conn.close()
    print(f"Database initialization complete")

if __name__ == "__main__":
    initialize_database()
