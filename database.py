# database.py
"""
Database helper module using SQLite.
Ensures schema is created and provides simple persistence.
"""

import sqlite3


class Database:
    def __init__(self, path="habits.db"):
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self):
        """Create tables if they do not exist."""
        cur = self.conn.cursor()

        # habits table
        cur.execute(
            """
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            frequency TEXT,
            description TEXT,
            goal INTEGER,
            created_at TEXT
        )
        """
        )

        # records table
        cur.execute(
            """
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER,
            date TEXT,
            value TEXT,
            completed_at TEXT,
            FOREIGN KEY (habit_id) REFERENCES habits(id)
        )
        """
        )

        # reduction plan table
        cur.execute(
            """
        CREATE TABLE IF NOT EXISTS reduction_plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER,
            baseline INTEGER,
            target INTEGER,
            step_size INTEGER,
            step_period_days INTEGER,
            start_date TEXT,
            target_date TEXT,
            FOREIGN KEY (habit_id) REFERENCES habits(id)
        )
        """
        )

        self.conn.commit()

    def cursor(self):
        return self.conn.cursor()

    def commit(self):
        self.conn.commit()
