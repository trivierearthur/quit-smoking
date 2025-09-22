import os
import random
import sqlite3
from itertools import groupby
from operator import itemgetter
from datetime import datetime, date, timedelta
from src import constants
from src import utils
from src.models import HabitModel, HabitRecordModel


class Database:
    def __init__(self, path=".db/tracker.db"):
        self.path = path
        self.conn = None

    def __enter__(self):
        # Ensure DB folder exists
        os.makedirs(os.path.dirname(self.path), exist_ok=True)

        # Connect to DB
        self.conn = sqlite3.connect(self.path)

        # Enable dict-like row access
        self.conn.row_factory = sqlite3.Row

        # Initialize tables and default data
        self._init_tables()
        self._add_default_data()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.commit()
            self.conn.close()

    def _get_cursor(self):
        if self.conn is None:
            raise RuntimeError("Database connection not initialized")
        return (self.conn.cursor(), self.conn.commit)

    def _init_tables(self):
        cursor, commit = self._get_cursor()

        cursor.execute(
            """CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                description TEXT,
                periodicity TEXT,
                habit_type TEXT,
                created TEXT
            )"""
        )

        cursor.execute(
            """CREATE TABLE IF NOT EXISTS records (
                day TEXT,
                habit_id INTEGER,
                value INTEGER,
                PRIMARY KEY (day, habit_id),
                FOREIGN KEY(habit_id) REFERENCES habits(id)
            )"""
        )
        commit()

    def _insert_record(self, day: str, habit_id: int, value: int):
        cursor, commit = self._get_cursor()

        cursor.execute(
            """INSERT OR REPLACE INTO records (day, habit_id, value)
            VALUES (?, ?, ?)""",
            (day, habit_id, value),
        )
        commit()

    def _insert_habit(
        self,
        name: str,
        description: str,
        periodicity: str,
        habit_type: str,
        habit_id: str | None = None,
    ):
        cursor, commit = self._get_cursor()

        datetime_now = datetime.now()

        cursor.execute(
            """INSERT INTO habits (id, name, description, periodicity, habit_type, created)
                VALUES (?, ?, ?, ?, ?, ?)""",
            (
                habit_id,
                name,
                description,
                periodicity,
                habit_type,
                datetime_now.isoformat(),
            ),
        )
        commit()

        return HabitModel(
            cursor.lastrowid,
            name,
            description,
            periodicity,
            habit_type,
            datetime_now,
            [],
        )

    def _count_habits(self) -> int:
        cursor, _commit = self._get_cursor()
        cursor.execute("SELECT COUNT(*) FROM habits")
        return cursor.fetchone()[0]

    def _add_default_data(self):
        habits_count = self._count_habits()

        if habits_count > 0:
            # Habits already exist, no need to add default data
            return

        today = date.today()

        for (
            habit_id,
            name,
            description,
            periodicity,
            habit_type,
        ) in constants.DEFAULT_HABITS:
            self._insert_habit(name, description, periodicity, habit_type, habit_id)

            if periodicity == constants.PERIODICITY_MONTHLY:
                self._insert_record(
                    utils.get_random_previous_day(
                        today, constants.DEFAULT_TIME_RANGE_IN_DAYS
                    ),
                    habit_id,
                    1,
                )
                continue

            if periodicity == constants.PERIODICITY_WEEKLY:
                for _ in range(4):
                    self._insert_record(
                        utils.get_random_previous_day(
                            today, constants.DEFAULT_TIME_RANGE_IN_DAYS
                        ),
                        habit_id,
                        1,
                    )
                continue

            if periodicity == constants.PERIODICITY_DAILY:
                for offset in range(constants.DEFAULT_TIME_RANGE_IN_DAYS):
                    daily_offset = (today - timedelta(days=offset + 1)).isoformat()
                    record_value = (
                        random.randint(1, 20)
                        if habit_id == constants.HABIT_CIGARETTE_SMOKED_ID
                        else random.randint(1, 10)
                    )
                    self._insert_record(daily_offset, habit_id, record_value)
                continue

    # Public methods

    def add_habit(
        self, name: str, desc: str, periodicity: str, habit_type: str
    ) -> HabitModel:
        return self._insert_habit(name, desc, periodicity, habit_type)

    def update_habit(
        self,
        habit_id: str,
        name: str,
        desc: str,
        periodicity: str,
        habit_type: str,
    ):
        cursor, commit = self._get_cursor()

        cursor.execute(
            "UPDATE habits SET name = ?, description = ?, periodicity = ?, habit_type = ? WHERE id = ?",
            (name, desc, periodicity, habit_type, habit_id),
        )
        commit()

    def delete_habit(self, habit_id: int):
        cursor, commit = self._get_cursor()

        cursor.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
        cursor.execute("DELETE FROM records WHERE habit_id = ?", (habit_id,))
        commit()

    def get_all_habits(self):
        cursor, _commit = self._get_cursor()

        cursor.execute("SELECT * FROM habits")
        habits_rows = cursor.fetchall()

        cursor.execute("SELECT * FROM records ORDER BY habit_id")
        records_rows = cursor.fetchall()

        records_by_habit = {
            hid: [
                HabitRecordModel(r["day"], r["habit_id"], int(r["value"])) for r in recs
            ]
            for hid, recs in groupby(records_rows, key=itemgetter("habit_id"))
        }

        return [
            HabitModel(
                h["id"],
                h["name"],
                h["description"],
                h["periodicity"],
                h["habit_type"],
                datetime.fromisoformat(h["created"]),
                records_by_habit.get(h["id"], []),
            )
            for h in habits_rows
        ]

    def update_record_value(self, day: str, habit_id: int, new_value: int):
        cursor, commit = self._get_cursor()

        cursor.execute(
            "UPDATE records SET value = ? WHERE day = ? AND habit_id = ?",
            (new_value, day, habit_id),
        )

        commit()

    def create_record(self, day: str, habit_id: int, value: int):
        self._insert_record(
            day,
            habit_id,
            value,
        )
