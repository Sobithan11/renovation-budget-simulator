import sqlite3
from pathlib import Path


DATABASE_FILE = Path(__file__).parent.parent / "database" / "renovation.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_FILE)
    connection.row_factory = sqlite3.Row
    return connection


def initialise_database():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            budget REAL NOT NULL,
            extension_size REAL DEFAULT 0,
            kitchen_spec TEXT DEFAULT 'standard',
            bathroom_spec TEXT DEFAULT 'standard',
            flooring_area REAL DEFAULT 0,
            electrical_work INTEGER DEFAULT 0,
            plumbing_work INTEGER DEFAULT 0,
            plastering_work INTEGER DEFAULT 0,
            painting_work INTEGER DEFAULT 0,
            windows_doors INTEGER DEFAULT 0,
            structural_work INTEGER DEFAULT 0,
            roofing_work INTEGER DEFAULT 0,
            landscaping_area REAL DEFAULT 0
        )
    """)

    connection.commit()
    connection.close()