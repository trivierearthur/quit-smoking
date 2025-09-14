"""
tracker.py
This module defines the HabitTracker class, which manages a collection of habits and provides methods to add, remove, modify, and log habits.
It also provides a function to generate reduction plans for quitting smoking.
"""

from src.habit import Habit


class HabitTracker:
    """
    Manages a collection of Habit objects, allowing add, remove, modify, and log operations.
    """

    def __init__(self):
        # List of all tracked habits
        self.habits = []

    def add_habit(self, habit: Habit):
        """Add a new habit to the tracker."""
        self.habits.append(habit)

    def remove_habit(self, habit_name):
        """Remove a habit by name from the tracker."""
        self.habits = [h for h in self.habits if h.name != habit_name]

    def modify_habit(
        self,
        old_name,
        new_name=None,
        new_desc=None,
        new_periodicity=None,
        new_type=None,
    ):
        """
        Modify the attributes of a habit identified by old_name.
        Only non-None arguments are updated.
        """
        habit = self.get_habit(old_name)
        if habit:
            if new_name:
                habit.name = new_name
            if new_desc:
                habit.description = new_desc
            if new_periodicity:
                habit.periodicity = new_periodicity
            if new_type:
                habit.type = new_type

    def get_habit(self, name):
        """Return the habit with the given name, or None if not found."""
        for h in self.habits:
            if h.name == name:
                return h
        return None

    def log_habit(self, habit_name, value):
        """Log a value for the habit with the given name."""
        habit = self.get_habit(habit_name)
        if habit:
            habit.log(value)


def generate_reduction_plan(cigarettes, gums, days=28):
    """
    Generate a reduction plan for cigarettes and gum over a given number of days.
    Returns a dict mapping habit names to a list of daily target values.
    """
    plan = {}
    for habit_name, start_value in [
        ("Cigarettes Smoked", cigarettes),
        ("Nicotine Gum Used", gums),
    ]:
        step = start_value / days
        plan[habit_name] = [max(0, round(start_value - i * step)) for i in range(days)]
    return plan
