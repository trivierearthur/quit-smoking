from tracker import HabitTracker
from habit import Habit


def test_add_and_get_habit():
    tracker = HabitTracker()
    habit = Habit("No Smoking", "desc", "daily", "elimination")
    tracker.add_habit(habit)
    assert tracker.get_habit("No Smoking") is habit


def test_remove_habit():
    tracker = HabitTracker()
    habit1 = Habit("No Smoking", "desc", "daily", "elimination")
    habit2 = Habit("Exercise", "desc", "daily", "establishment")
    tracker.add_habit(habit1)
    tracker.add_habit(habit2)
    tracker.remove_habit("No Smoking")
    assert tracker.get_habit("No Smoking") is None
    assert tracker.get_habit("Exercise") is habit2


def test_modify_habit():
    tracker = HabitTracker()
    habit = Habit("No Smoking", "desc", "daily", "elimination")
    tracker.add_habit(habit)
    tracker.modify_habit(
        "No Smoking",
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
    tracker = HabitTracker()
    habit = Habit("No Smoking", "desc", "daily", "elimination")
    tracker.add_habit(habit)
    called = {}

    def fake_log(value, date=None):
        called["value"] = value

    habit.log = fake_log
    tracker.log_habit("No Smoking", 5)
    assert called["value"] == 5


def test_get_habit_returns_none_for_missing():
    tracker = HabitTracker()
    assert tracker.get_habit("Nonexistent") is None
