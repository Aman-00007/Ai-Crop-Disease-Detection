# db.py

import sqlite3
from datetime import datetime

DB_NAME = 'database/users.db'

def create_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn

def init_db():
    conn = create_connection()
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            location TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    ''')

    # Create tests table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            image_path TEXT NOT NULL,
            prediction TEXT NOT NULL,
            treatment TEXT NOT NULL,
            confidence REAL,
            tested_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    ''')

    # Lightweight migration: add confidence column to older databases
    cursor.execute("PRAGMA table_info(tests)")
    columns = [row[1] for row in cursor.fetchall()]
    if 'confidence' not in columns:
        cursor.execute("ALTER TABLE tests ADD COLUMN confidence REAL")

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("✅ Database initialized and tables created.")
