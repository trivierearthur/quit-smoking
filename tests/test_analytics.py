import datetime
from src.analytics import (
    list_habits,
    habits_by_periodicity,
    longest_streak,
    longest_streak_all,
    plot_habit_time_series,
)
from src.habit import Habit
from src.tracker import HabitTracker


def test_list_habits():
    tracker = HabitTracker()
    h1 = Habit("No Smoking", "desc", "daily", "elimination")
    h2 = Habit("Exercise", "desc", "weekly", "establishment")
    tracker.add_habit(h1)
    tracker.add_habit(h2)
    assert set(list_habits(tracker)) == {"No Smoking", "Exercise"}


def test_habits_by_periodicity():
    tracker = HabitTracker()
    h1 = Habit("No Smoking", "desc", "daily", "elimination")
    h2 = Habit("Exercise", "desc", "weekly", "establishment")
    tracker.add_habit(h1)
    tracker.add_habit(h2)
    assert habits_by_periodicity(tracker, "daily") == ["No Smoking"]
    assert habits_by_periodicity(tracker, "weekly") == ["Exercise"]


def test_longest_streak():
    habit = Habit("Test", "desc", "daily", "elimination")
    # No records
    assert longest_streak(habit) == 0
    # 3-day streak
    base = datetime.date(2025, 9, 10)
    for i in range(3):
        habit.log(1, date=base + datetime.timedelta(days=i))
    assert longest_streak(habit) == 3
    # Break in streak
    habit.log(1, date=base + datetime.timedelta(days=5))
    assert longest_streak(habit) == 3


def test_longest_streak_all():
    tracker = HabitTracker()
    h1 = Habit("A", "desc", "daily", "elimination")
    h2 = Habit("B", "desc", "daily", "elimination")
    base = datetime.date(2025, 9, 10)
    for i in range(2):
        h1.log(1, date=base + datetime.timedelta(days=i))
    for i in range(4):
        h2.log(1, date=base + datetime.timedelta(days=i))
    tracker.add_habit(h1)
    tracker.add_habit(h2)
    assert longest_streak_all(tracker) == 4


def test_plot_habit_time_series(monkeypatch):
    habit = Habit("Test", "desc", "daily", "elimination")
    base = datetime.date(2025, 9, 10)
    for i in range(3):
        habit.log(i, date=base + datetime.timedelta(days=i))
    called = {}

    def fake_show():
        called["shown"] = True

    monkeypatch.setattr("matplotlib.pyplot.show", fake_show)
    plot_habit_time_series(habit)
    assert called.get("shown")


def test_plot_habit_time_series_no_data(capsys):
    habit = Habit("Test", "desc", "daily", "elimination")
    plot_habit_time_series(habit)
    captured = capsys.readouterr()
    assert "No data for Test" in captured.out
