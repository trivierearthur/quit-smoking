import sqlite3
import datetime
from src.persistence import init_db, save_habit, load_tracker
from src.habit import Habit


def test_init_db_creates_tables(tmp_path, monkeypatch):
    # Use a temporary file for the database
    db_file = tmp_path / "test_tracker.db"
    monkeypatch.setattr("src.persistence.DB_FILE", str(db_file))
    init_db()
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='habits'")
    assert c.fetchone() is not None
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='records'")
    assert c.fetchone() is not None
    conn.close()

    assert True
    db_file = tmp_path / "test_tracker.db"
    monkeypatch.setattr("src.persistence.DB_FILE", str(db_file))
    init_db()
    habit = Habit(
        "Test", "desc", "daily", "elimination", created=datetime.datetime(2025, 9, 13)
    )
    habit.log(5, date=datetime.date(2025, 9, 13))
    save_habit(habit)
    tracker = load_tracker()
    loaded = tracker.get_habit("Test")
    assert loaded is not None
    assert loaded.name == "Test"
    assert loaded.description == "desc"
    assert loaded.periodicity == "daily"
    assert loaded.type == "elimination"
    assert loaded.created == datetime.datetime(2025, 9, 13)
    assert loaded.records[datetime.date(2025, 9, 13)] == 5
