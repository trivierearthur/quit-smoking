import datetime
from src.analytics import (
    list_habits,
    habits_by_periodicity,
    longest_run_streak_for_habit,
    longest_run_streak_all,
)
from src.habit import Habit
from src.tracker import HabitTracker


def test_list_habits():
    # Test that all habit names are listed from the tracker
    tracker = HabitTracker()
    h1 = Habit("Cigarettes Smoked", "desc", "daily", "elimination")
    h2 = Habit("Nicotine Gum Used", "desc", "daily", "elimination")
    tracker.add_habit(h1)
    tracker.add_habit(h2)
    assert set(list_habits(tracker)) == {"Cigarettes Smoked", "Nicotine Gum Used"}


def test_habits_by_periodicity():
    # Test that habits are filtered by periodicity
    tracker = HabitTracker()
    h1 = Habit("Cigarettes Smoked", "desc", "daily", "elimination")
    h2 = Habit("Nicotine Gum Used", "desc", "weekly", "elimination")
    tracker.add_habit(h1)
    tracker.add_habit(h2)
    assert habits_by_periodicity(tracker, "daily") == ["Cigarettes Smoked"]
    assert habits_by_periodicity(tracker, "weekly") == ["Nicotine Gum Used"]


def test_longest_run_streak_for_habit():
    # Test the longest streak calculation for a single habit
    habit = Habit("Cigarettes Smoked", "desc", "daily", "elimination")
    base = datetime.date.today()
    for i in range(3):
        habit.log(1, date=base + datetime.timedelta(days=i))
    assert longest_run_streak_for_habit(habit) == 3


def test_longest_run_streak_all():
    # Test the longest streak calculation across all habits in the tracker
    tracker = HabitTracker()
    h1 = Habit("Cigarettes Smoked", "desc", "daily", "elimination")
    h2 = Habit("Nicotine Gum Used", "desc", "daily", "elimination")
    base = datetime.date.today()
    for i in range(2):
        h1.log(1, date=base + datetime.timedelta(days=i))
    for i in range(4):
        h2.log(1, date=base + datetime.timedelta(days=i))
    tracker.add_habit(h1)
    tracker.add_habit(h2)
    assert longest_run_streak_all(tracker) == 4
