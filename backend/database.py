import os
import psycopg2
import psycopg2.extras


def get_connection():
    """
    Create a PostgreSQL database connection using DATABASE_URL.
    Returns a connection whose cursor can return dict-like rows.
    """
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise RuntimeError("DATABASE_URL is not set. Add it to your environment variables.")

    # Dict-like rows
    conn = psycopg2.connect(db_url, cursor_factory=psycopg2.extras.RealDictCursor)
    return conn


def init_db():
    """
    Create the required tables if they don't exist, and evolve schema safely.

    Postgres notes:
    - Uses CREATE TABLE IF NOT EXISTS
    - Uses ALTER TABLE ADD COLUMN IF NOT EXISTS (safe schema evolution)
    - Enforces one entry per user per day via UNIQUE(user_id, entry_date)
    """
    conn = get_connection()
    cur = conn.cursor()

    # --- Users table ---
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id BIGSERIAL PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            email TEXT UNIQUE,
            password_hash TEXT NOT NULL,
            is_verified BOOLEAN DEFAULT FALSE,
            verification_token TEXT,
            verification_sent_at TIMESTAMPTZ,
            created_at TIMESTAMPTZ DEFAULT NOW()
        );
        """
    )

    # --- Health logs table ---
    # Use DATE instead of TEXT for entry_date (better querying + comparisons)
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS health_logs (
            id BIGSERIAL PRIMARY KEY,
            user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
            entry_date DATE NOT NULL,
            weight DOUBLE PRECISION,
            steps INTEGER,
            water_intake DOUBLE PRECISION,
            sleep_hours DOUBLE PRECISION,
            created_at TIMESTAMPTZ DEFAULT NOW(),
            CONSTRAINT uq_health_user_date UNIQUE (user_id, entry_date)
        );
        """
    )

    # ---- Schema evolution (if your old DB schema is missing columns) ----
    # These are safe even if the column already exists.
    cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS email TEXT;")
    cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS is_verified BOOLEAN DEFAULT FALSE;")
    cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS verification_token TEXT;")
    cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS verification_sent_at TIMESTAMPTZ;")
    cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ DEFAULT NOW();")

    cur.execute("ALTER TABLE health_logs ADD COLUMN IF NOT EXISTS user_id BIGINT;")
    cur.execute("ALTER TABLE health_logs ADD COLUMN IF NOT EXISTS entry_date DATE;")
    cur.execute("ALTER TABLE health_logs ADD COLUMN IF NOT EXISTS weight DOUBLE PRECISION;")
    cur.execute("ALTER TABLE health_logs ADD COLUMN IF NOT EXISTS steps INTEGER;")
    cur.execute("ALTER TABLE health_logs ADD COLUMN IF NOT EXISTS water_intake DOUBLE PRECISION;")
    cur.execute("ALTER TABLE health_logs ADD COLUMN IF NOT EXISTS sleep_hours DOUBLE PRECISION;")
    cur.execute("ALTER TABLE health_logs ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ DEFAULT NOW();")

    # Ensure FK exists (older DB might not have it). This is a safe pattern:
    # Create constraint only if not exists (Postgres doesn't support IF NOT EXISTS for ADD CONSTRAINT directly),
    # so we check in pg_constraint first.
    cur.execute(
        """
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1
                FROM pg_constraint
                WHERE conname = 'fk_health_logs_user'
            ) THEN
                ALTER TABLE health_logs
                ADD CONSTRAINT fk_health_logs_user
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;
            END IF;
        END $$;
        """
    )

    # Ensure unique constraint exists (same issue: no IF NOT EXISTS for constraint name)
    cur.execute(
        """
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1
                FROM pg_constraint
                WHERE conname = 'uq_health_user_date'
            ) THEN
                ALTER TABLE health_logs
                ADD CONSTRAINT uq_health_user_date UNIQUE (user_id, entry_date);
            END IF;
        END $$;
        """
    )

    # Helpful indexes (optional but good)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_health_logs_user_id ON health_logs(user_id);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_health_logs_entry_date ON health_logs(entry_date);")

    conn.commit()
    cur.close()
    conn.close()
