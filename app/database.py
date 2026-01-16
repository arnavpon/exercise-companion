import libsql_client
from app.config import TURSO_DATABASE_URL, TURSO_AUTH_TOKEN, EQUIPMENT_TYPES

_client = None


def get_db():
    """Get database client (singleton)."""
    global _client
    if _client is None:
        _client = libsql_client.create_client_sync(
            url=TURSO_DATABASE_URL,
            auth_token=TURSO_AUTH_TOKEN,
        )
    return _client


def init_db():
    """Initialize database schema."""
    client = get_db()

    # Create tables
    client.execute("""
        CREATE TABLE IF NOT EXISTS movements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    """)

    client.execute("""
        CREATE TABLE IF NOT EXISTS equipment_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    """)

    client.execute("""
        CREATE TABLE IF NOT EXISTS weightlifting_set (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            movement TEXT NOT NULL,
            equipment_type TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            n_of_reps INTEGER NOT NULL,
            weight REAL NOT NULL
        )
    """)

    client.execute("""
        CREATE TABLE IF NOT EXISTS cardio_set (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            movement TEXT NOT NULL,
            equipment_type TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            distance REAL NOT NULL,
            duration REAL NOT NULL,
            power_output REAL DEFAULT 0
        )
    """)

    # Create indexes
    client.execute(
        "CREATE INDEX IF NOT EXISTS idx_weightlifting_movement ON weightlifting_set(movement)"
    )
    client.execute(
        "CREATE INDEX IF NOT EXISTS idx_weightlifting_timestamp ON weightlifting_set(timestamp)"
    )

    # Seed default equipment types
    for eq_type in EQUIPMENT_TYPES:
        try:
            client.execute(
                "INSERT OR IGNORE INTO equipment_types (name) VALUES (?)", [eq_type]
            )
        except Exception:
            pass

    # Seed default movements table if empty
    try:
        client.execute("INSERT OR IGNORE INTO movements (name) VALUES (?)", ["bench press"])
    except Exception:
        pass
