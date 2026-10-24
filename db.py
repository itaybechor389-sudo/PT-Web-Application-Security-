import sqlite3
from pathlib import Path
from contextlib import closing

DB_PATH = Path(__file__).resolve().parent / "users.db"


def init_db():
    with closing(sqlite3.connect(DB_PATH)) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        with connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT NOT NULL UNIQUE COLLATE NOCASE,
                    password_hash TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """)
            connection.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    token_hash TEXT PRIMARY KEY NOT NULL,
                    user_id INTEGER NOT NULL,
                    expires_at INTEGER NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                        ON DELETE CASCADE
                )
            """)


if __name__ == "__main__":
    init_db()
    print(f"Database ready: {DB_PATH}")
