import sqlite3
from pathlib import Path


DATABASE_DIRECTORY = Path(__file__).parent.parent / "database"
DATABASE_FILE = DATABASE_DIRECTORY / "renovation.db"


def get_connection():
    DATABASE_DIRECTORY.mkdir(parents=True, exist_ok=True)

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
            painting_area REAL DEFAULT 0,
            windows_doors INTEGER DEFAULT 0,
            structural_work INTEGER DEFAULT 0,
            roofing_work INTEGER DEFAULT 0,
            landscaping_area REAL DEFAULT 0
        )
    """)

    connection.commit()
    connection.close()