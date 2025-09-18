from src.tracker import HabitTracker
from src.habit import Habit


def test_add_and_get_habit():
    # Test that a habit can be added and retrieved by name
    tracker = HabitTracker()
    habit = Habit("Cigarettes Smoked", "desc", "daily", "elimination")
    tracker.add_habit(habit)
    assert tracker.get_habit("Cigarettes Smoked") is habit


def test_remove_habit():
    # Test that a habit can be removed and others remain
    tracker = HabitTracker()
    habit1 = Habit("Cigarettes Smoked", "desc", "daily", "elimination")
    habit2 = Habit("Nicotine Gum Used", "desc", "daily", "elimination")
    tracker.add_habit(habit1)
    tracker.add_habit(habit2)
    tracker.remove_habit("Cigarettes Smoked")
    assert tracker.get_habit("Cigarettes Smoked") is None
    assert tracker.get_habit("Nicotine Gum Used") is habit2


def test_modify_habit():
    # Test that a habit's attributes can be modified
    tracker = HabitTracker()
    habit = Habit("Cigarettes Smoked", "desc", "daily", "elimination")
    tracker.add_habit(habit)
    tracker.modify_habit(
        "Cigarettes Smoked",
        new_name="Quit Smoking",
        new_desc="new desc",
        new_periodicity="weekly",
        new_type="establishment",
    )
    modified = tracker.get_habit("Quit Smoking")
    assert modified is not None
    assert modified.name == "Quit Smoking"
    assert modified.description == "new desc"
    assert modified.periodicity == "weekly"
    assert modified.type == "establishment"


def test_log_habit():
    # Test that logging a value for a habit calls the habit's log method
    tracker = HabitTracker()
    habit = Habit("Cigarettes Smoked", "desc", "daily", "elimination")
    tracker.add_habit(habit)
    called = {}

    def fake_log(value, date=None):
        called["value"] = value

    habit.log = fake_log
    tracker.log_habit("Cigarettes Smoked", 5)
    assert called["value"] == 5


def test_get_habit_returns_none_for_missing():
    # Test that getting a non-existent habit returns None
    tracker = HabitTracker()
    assert tracker.get_habit("Nonexistent") is None
