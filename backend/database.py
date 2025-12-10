
import sqlite3
from pathlib import Path

# Path to the SQLite DB file (health.db in backend folder)
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "health.db"


def get_connection():
    """
    Create a database connection and return the connection object.
    """
    conn = sqlite3.connect(DB_PATH)
    # Return rows as dict-like objects
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """
    Create the health_logs table if it doesn't exist.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS health_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entry_date TEXT NOT NULL,
            weight REAL,
            steps INTEGER,
            water_intake REAL,
            sleep_hours REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    )

    conn.commit()
    conn.close()
