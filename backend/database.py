
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
    Create the required tables if they don't exist.

    Notes (SQLite):
    - If you already created health.db earlier, this function will try to
      evolve the schema (add user_id + unique index) without deleting data.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # --- Users table (very small auth layer) ---
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT UNIQUE,
            password_hash TEXT NOT NULL,
            is_verified INTEGER DEFAULT 0,
            verification_token TEXT,
            verification_sent_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS health_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            entry_date TEXT NOT NULL,
            weight REAL,
            steps INTEGER,
            water_intake REAL,
            sleep_hours REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ,FOREIGN KEY (user_id) REFERENCES users(id)
        );
        """
    )

    # If an older DB exists without user_id, add the column.
    cursor.execute("PRAGMA table_info(health_logs);")
    cols = [r[1] for r in cursor.fetchall()]  # (cid, name, type, notnull, dflt, pk)
    if "user_id" not in cols:
        cursor.execute("ALTER TABLE health_logs ADD COLUMN user_id INTEGER;")

    # If users table exists but older schema missing new columns, add them
    cursor.execute("PRAGMA table_info(users);")
    user_cols = [r[1] for r in cursor.fetchall()]
    if "email" not in user_cols:
        cursor.execute("ALTER TABLE users ADD COLUMN email TEXT;")
    if "is_verified" not in user_cols:
        cursor.execute("ALTER TABLE users ADD COLUMN is_verified INTEGER DEFAULT 0;")
    if "verification_token" not in user_cols:
        cursor.execute("ALTER TABLE users ADD COLUMN verification_token TEXT;")
    if "verification_sent_at" not in user_cols:
        cursor.execute("ALTER TABLE users ADD COLUMN verification_sent_at TIMESTAMP;")

    # Enforce: one entry per user per day
    cursor.execute(
        """
        CREATE UNIQUE INDEX IF NOT EXISTS idx_health_user_date
        ON health_logs(user_id, entry_date);
        """
    )

    # Add unique index on email for quick lookup and uniqueness (if not exist)
    cursor.execute(
        """
        CREATE UNIQUE INDEX IF NOT EXISTS idx_users_email
        ON users(email);
        """
    )

    conn.commit()
    conn.close()
