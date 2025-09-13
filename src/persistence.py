import sqlite3
from src.habit import Habit
from src.tracker import HabitTracker
import datetime

DB_FILE = ".db/tracker.db"


def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS habits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE,
                    description TEXT,
                    periodicity TEXT,
                    type TEXT,
                    created TEXT)"""
    )
    c.execute(
        """CREATE TABLE IF NOT EXISTS records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    habit_id INTEGER,
                    record_date TEXT,
                    value INTEGER,
                    FOREIGN KEY(habit_id) REFERENCES habits(id))"""
    )
    conn.commit()
    conn.close()


def save_habit(habit: Habit):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        """INSERT OR IGNORE INTO habits(name, description, periodicity, type, created)
                 VALUES (?, ?, ?, ?, ?)""",
        (
            habit.name,
            habit.description,
            habit.periodicity,
            habit.type,
            habit.created.isoformat(),
        ),
    )
    c.execute("SELECT id FROM habits WHERE name=?", (habit.name,))
    habit_id = c.fetchone()[0]
    for date, value in habit.records.items():
        c.execute(
            """INSERT OR REPLACE INTO records(habit_id, record_date, value)
                     VALUES (?, ?, ?)""",
            (habit_id, date.isoformat(), value),
        )
    conn.commit()
    conn.close()


def load_tracker():
    tracker = HabitTracker()
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM habits")
    habit_rows = c.fetchall()
    for h_row in habit_rows:
        habit = Habit(
            h_row[1],
            h_row[2],
            h_row[3],
            h_row[4],
            created=datetime.datetime.fromisoformat(h_row[5]),
        )
        habit_id = h_row[0]
        c.execute(
            "SELECT record_date, value FROM records WHERE habit_id=?", (habit_id,)
        )
        for r_row in c.fetchall():
            habit.records[datetime.date.fromisoformat(r_row[0])] = r_row[1]
            habit.time_series[datetime.date.fromisoformat(r_row[0])] = r_row[1]
        tracker.add_habit(habit)
    conn.close()
    return tracker
