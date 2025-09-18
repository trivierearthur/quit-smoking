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
    # Test that prior data for 'Cigarettes Smoked' uses initial value
    data = generate_prior_data("Cigarettes Smoked", initial_value=20)
    assert len(data) == 28
    assert data[0] == 20
    # Test that unknown habit returns 28 zeros
    data = generate_prior_data("Unknown")
    assert data == [0] * 28


def test_setup_initial_consumption(monkeypatch):
    # Simulate user input for cigarettes and gum
    inputs = iter(["20", "15"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    tracker = HabitTracker()
    result = setup_initial_consumption(tracker)
    assert result == {"Cigarettes Smoked": 20, "Nicotine Gum Used": 15}
    assert tracker.get_habit("Cigarettes Smoked") is not None
    assert tracker.get_habit("Nicotine Gum Used") is not None


def test_show_dashboard(capsys):
    tracker = HabitTracker()
    tracker.add_habit(Habit("Cigarettes Smoked", "desc", "daily", "elimination"))
    show_dashboard(tracker)
    captured = capsys.readouterr()
    assert "Cigarettes Smoked" in captured.out


def test_show_reduction_plans(capsys):
    tracker = HabitTracker()
    h = Habit("Cigarettes Smoked", "desc", "daily", "elimination")
    h.plan = [20, 19, 18, 17]
    tracker.add_habit(h)
    show_reduction_plans(tracker)
    captured = capsys.readouterr()
    assert "Plan for Cigarettes Smoked" in captured.out


def test_log_habit_values(monkeypatch):
    tracker = HabitTracker()
    h = Habit("Cigarettes Smoked", "desc", "daily", "elimination")
    tracker.add_habit(h)
    monkeypatch.setattr("builtins.input", lambda _: "7")
    log_habit_values(tracker)
    assert h.records


def test_add_habit(monkeypatch):
    tracker = HabitTracker()
    inputs = iter(["Test", "desc", "daily", "elimination"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    add_habit(tracker)
    assert tracker.get_habit("Test") is not None


def test_remove_habit(monkeypatch):
    tracker = HabitTracker()
    h = Habit("Test", "desc", "daily", "elimination")
    tracker.add_habit(h)
    monkeypatch.setattr("builtins.input", lambda _: "Test")
    remove_habit(tracker)
    assert tracker.get_habit("Test") is None


def test_modify_habit(monkeypatch):
    tracker = HabitTracker()
    h = Habit("Test", "desc", "daily", "elimination")
    tracker.add_habit(h)
    inputs = iter(["Test", "NewName", "NewDesc", "weekly", "establishment"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    modify_habit(tracker)
    modified = tracker.get_habit("NewName")
    assert modified is not None
    assert modified.description == "NewDesc"
    assert modified.periodicity == "weekly"
    assert modified.type == "establishment"


def test_show_analytics(capsys):
    tracker = HabitTracker()
    h = Habit("Cigarettes Smoked", "desc", "daily", "elimination")
    tracker.add_habit(h)
    show_analytics(tracker)
    captured = capsys.readouterr()
    assert "Tracked habits" in captured.out
