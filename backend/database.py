import os
import sqlite3
from pathlib import Path
from urllib.parse import urlparse

# Optional: if you install psycopg2-binary, we can use Postgres on Render
try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
except Exception:
    psycopg2 = None
    RealDictCursor = None


BASE_DIR = Path(__file__).resolve().parent
SQLITE_PATH = BASE_DIR / "health.db"


def is_postgres_url(db_url: str | None) -> bool:
    if not db_url:
        return False
    return db_url.startswith("postgres://") or db_url.startswith("postgresql://")


def get_db_url() -> str | None:
    # Render provides DATABASE_URL for Postgres if you set it
    return os.getenv("DATABASE_URL")


def get_connection():
    """
    Returns a live DB connection.
    - Postgres if DATABASE_URL starts with postgres/postgresql
    - Otherwise SQLite (health.db) for local dev
    """
    db_url = get_db_url()

    if is_postgres_url(db_url):
        if psycopg2 is None:
            raise RuntimeError("psycopg2-binary not installed but DATABASE_URL is Postgres.")
        # RealDictCursor makes fetchone()/fetchall() return dict rows like sqlite Row factory
        return psycopg2.connect(db_url, cursor_factory=RealDictCursor)

    # SQLite fallback
    conn = sqlite3.connect(SQLITE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _execute(conn, sql: str, params: tuple = ()):
    """
    Execute SQL and return cursor.
    Normalizes placeholders:
    - If Postgres: use %s
    - If SQLite: use ?
    """
    cur = conn.cursor()

    # If using Postgres, ensure placeholders are %s
    if is_postgres_url(get_db_url()):
        # Convert SQLite-style ? placeholders to %s if someone wrote SQLite queries
        if "?" in sql:
            sql = sql.replace("?", "%s")
    else:
        # If using SQLite, convert %s to ? if someone wrote Postgres queries
        if "%s" in sql:
            sql = sql.replace("%s", "?")

    cur.execute(sql, params)
    return cur


def init_db():
    """
    Create required tables if they don't exist.
    Works for both SQLite + Postgres.
    """
    conn = get_connection()
    try:
        if is_postgres_url(get_db_url()):
            # Postgres schema
            _execute(conn, """
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username TEXT NOT NULL UNIQUE,
                    email TEXT UNIQUE,
                    password_hash TEXT NOT NULL,
                    is_verified BOOLEAN DEFAULT TRUE,
                    verification_token TEXT,
                    verification_sent_at TIMESTAMP,
                    created_at TIMESTAMP DEFAULT NOW()
                )
            """)
            conn.commit()
        else:
            # SQLite schema
            _execute(conn, """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    email TEXT UNIQUE,
                    password_hash TEXT NOT NULL,
                    is_verified INTEGER DEFAULT 1,
                    verification_token TEXT,
                    verification_sent_at TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
    finally:
        conn.close()
