from datetime import date
from src.db import Database
from src import constants
from src.models import HabitModel


class Habit:
    def __init__(self, habit_model: HabitModel):
        self.id = habit_model.id
        self.name = habit_model.name
        self.description = habit_model.description
        self.periodicity = habit_model.periodicity
        self.habit_type = habit_model.habit_type
        self.created = habit_model.created
        self.records = {record.day: record.value for record in habit_model.records}


class HabitManager:
    """
    Manages a collection of Habit objects, allowing add, remove, modify, and log operations.
    """

    def __init__(self, db: Database):
        self.db = db
        self.habits: list[Habit] = []

    def load_habits(self):
        self.habits = [Habit(db_model) for db_model in self.db.get_all_habits()]

    def _get_habit_by_id(self, habit_id: int):
        """Get a habit by its id."""
        habit = next(
            (h for h in self.habits if getattr(h, "id", None) == habit_id), None
        )
        if habit is None:
            raise ValueError(f"Habit with id {habit_id} not found.")
        return habit

    def _get_habit_by_name(self, habit_name: str):
        """Get a habit by its id."""
        habit = next(
            (h for h in self.habits if getattr(h, "name", None) == habit_name), None
        )
        return habit

    def _get_today_key(self):
        return date.today().isoformat()

    # CLI calls

    def add_habit(self, name: str, desc: str, periodicity: str, habit_type: str):
        """Add a new habit to the tracker."""

        existing_habit = self._get_habit_by_name(name)

        if existing_habit is not None:
            raise ValueError(f"Habit with name '{name}' already exists.")

        added_habit = self.db.add_habit(name, desc, periodicity, habit_type)
        self.habits.append(Habit(added_habit))

    def update_habit(
        self, name: str, new_name: str, desc: str, periodicity: str, habit_type: str
    ):
        """Add a new habit to the tracker."""

        existing_habit = self._get_habit_by_name(name)

        if existing_habit is None:
            return

        existing_habit.name = new_name
        existing_habit.description = desc
        existing_habit.periodicity = periodicity
        existing_habit.habit_type = habit_type

        self.db.update_habit(existing_habit.id, new_name, desc, periodicity, habit_type)

    def remove_habit(self, habit_name: str):
        """Remove a habit by name from the tracker."""
        existing_habit = self._get_habit_by_name(habit_name)

        if existing_habit is None:
            return

        self.habits = [h for h in self.habits if h.name != habit_name]
        self.db.delete_habit(existing_habit.id)

    def log_today_habit(self, habit_id: int, value: int):
        """Log or update today's record for a habit."""
        today = self._get_today_key()
        habit = self._get_habit_by_id(habit_id)

        # Try to find today's record in the habit
        existing_record = habit.records.get(today)

        if existing_record is not None:
            # Update existing record in memory
            habit.records[today] = value
            # Update in database
            self.db.update_record_value(today, habit_id, value)
        else:
            # Create a new record in memory
            habit.records[today] = value
            # Insert in database
            self.db.create_record(today, habit_id, value)

    def get_today_habit_value(self, habit_id: int) -> int:
        """Log a value for the habit with the given name."""

        habit = self._get_habit_by_id(habit_id)
        today_record = habit.records.get(self._get_today_key())

        return today_record if today_record is not None else 0

    def has_no_elimination_daily_logs(self) -> bool:
        return any(
            self.get_today_habit_value(habit.id) == 0
            for habit in self.habits
            if habit.habit_type == constants.HABIT_TYPE_ELIMINATION
        )
