import sqlite3
from pathlib import Path
from config import DB_FILE, EDGE_TABLE_NAME, EDGE_INDEX_PREFIX

def initialize_database():
    db_file = Path(DB_FILE)

    if db_file.exists():
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (EDGE_TABLE_NAME,))
        if cursor.fetchone():
            conn.close()
            return
        conn.close()

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS {EDGE_TABLE_NAME} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_id TEXT NOT NULL,
        target_id TEXT NOT NULL,
        relationship_type TEXT NOT NULL,
        strength REAL,
        confidence REAL,
        bidirectional BOOLEAN,
        start_time TIMESTAMP,
        end_time TIMESTAMP,
        metadata JSON,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    cursor.execute(f'CREATE INDEX IF NOT EXISTS {EDGE_INDEX_PREFIX}source ON {EDGE_TABLE_NAME} (source_id)')
    cursor.execute(f'CREATE INDEX IF NOT EXISTS {EDGE_INDEX_PREFIX}target ON {EDGE_TABLE_NAME} (target_id)')
    cursor.execute(f'CREATE INDEX IF NOT EXISTS {EDGE_INDEX_PREFIX}relationship ON {EDGE_TABLE_NAME} (relationship_type)')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS node_attributes (
        node_id TEXT NOT NULL,
        attribute_name TEXT NOT NULL,
        attribute_value TEXT,
        confidence REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (node_id, attribute_name)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS hierarchies (
        parent_id TEXT NOT NULL,
        child_id TEXT NOT NULL,
        hierarchy_type TEXT NOT NULL,
        confidence REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (parent_id, child_id, hierarchy_type)
    )
    ''')

    cursor.execute(f'''
    CREATE TRIGGER IF NOT EXISTS update_{EDGE_TABLE_NAME}_timestamp
    AFTER UPDATE ON {EDGE_TABLE_NAME}
    BEGIN
        UPDATE {EDGE_TABLE_NAME} SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;
    ''')

    cursor.execute('''
    CREATE TRIGGER IF NOT EXISTS update_node_attributes_timestamp
    AFTER UPDATE ON node_attributes
    BEGIN
        UPDATE node_attributes SET updated_at = CURRENT_TIMESTAMP
        WHERE node_id = NEW.node_id AND attribute_name = NEW.attribute_name;
    END;
    ''')

    cursor.execute('''
    CREATE TRIGGER IF NOT EXISTS update_hierarchies_timestamp
    AFTER UPDATE ON hierarchies
    BEGIN
        UPDATE hierarchies SET updated_at = CURRENT_TIMESTAMP
        WHERE parent_id = NEW.parent_id AND child_id = NEW.child_id AND hierarchy_type = NEW.hierarchy_type;
    END;
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_database()
