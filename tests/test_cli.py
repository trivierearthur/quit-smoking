from src.cli import (
    generate_prior_data,
    setup_initial_consumption,
    show_dashboard,
    show_reduction_plans,
    log_habit_values,
    add_habit,
    remove_habit,
    modify_habit,
    show_analytics,
)
from src.tracker import HabitTracker
from src.habit import Habit


def test_generate_prior_data():
    # Test that prior data for 'Cigarettes Smoked' is 28 integers
    data = generate_prior_data("Cigarettes Smoked")
    assert len(data) == 28
    assert all(isinstance(x, int) for x in data)
    # Test that unknown habit returns 28 zeros
    data = generate_prior_data("Unknown")
    assert data == [0] * 28


def test_setup_initial_consumption(monkeypatch):
    # Simulate user entering 5 for cigarettes and 2 for gum
    inputs = iter(["5", "2"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    result = setup_initial_consumption()
    # Check the returned dictionary matches the simulated input
    assert result == {"Cigarettes Smoked": 5, "Nicotine Gum Used": 2}


def test_show_dashboard(capsys):
    # Add a habit and check it appears in dashboard output
    tracker = HabitTracker()
    tracker.add_habit(Habit("Test", "desc", "daily", "elimination"))
    show_dashboard(tracker)
    captured = capsys.readouterr()
    assert "Test" in captured.out


def test_show_reduction_plans(capsys):
    # Add a habit with a plan and check the plan is displayed
    tracker = HabitTracker()
    h = Habit("Test", "desc", "daily", "elimination")
    h.plan = [1, 2, 3, 4, 5, 6, 7]
    tracker.add_habit(h)
    show_reduction_plans(tracker)
    captured = capsys.readouterr()
    assert "Plan for Test" in captured.out
    assert "1, 2, 3, 4, 5, 6, 7" in captured.out


def test_log_habit_values(monkeypatch):
    # Simulate logging a value for a habit and check records are updated
    tracker = HabitTracker()
    h = Habit("Test", "desc", "daily", "elimination")
    tracker.add_habit(h)
    monkeypatch.setattr("builtins.input", lambda _: "7")
    log_habit_values(tracker)
    assert h.records


def test_add_habit(monkeypatch):
    # Simulate user input to add a habit and check it is added
    tracker = HabitTracker()
    inputs = iter(["Test", "desc", "daily", "elimination"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    add_habit(tracker)
    assert tracker.get_habit("Test") is not None


def test_remove_habit(monkeypatch):
    # Add a habit, simulate input to remove it, and check it is removed
    tracker = HabitTracker()
    h = Habit("Test", "desc", "daily", "elimination")
    tracker.add_habit(h)
    monkeypatch.setattr("builtins.input", lambda _: "Test")
    remove_habit(tracker)
    assert tracker.get_habit("Test") is None


def test_modify_habit(monkeypatch):
    # Add a habit, simulate input to modify it, and check all fields are updated
    tracker = HabitTracker()
    h = Habit("Test", "desc", "daily", "elimination")
    tracker.add_habit(h)
    # old_name, new_name, new_desc, new_periodicity, new_type
    inputs = iter(["Test", "NewName", "NewDesc", "weekly", "establishment"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    modify_habit(tracker)
    modified = tracker.get_habit("NewName")
    assert modified is not None
    assert modified.description == "NewDesc"
    assert modified.periodicity == "weekly"
    assert modified.type == "establishment"


def test_show_analytics(capsys):
    # Add a habit and check analytics output includes expected text
    tracker = HabitTracker()
    h = Habit("Test", "desc", "daily", "elimination")
    tracker.add_habit(h)
    show_analytics(tracker)
    captured = capsys.readouterr()
    assert "Tracked habits" in captured.out
