# CLI module: Handles user interaction, menu logic, and connects tracker, habit, and analytics modules.
from src.tracker import HabitTracker
from src.habit import Habit
from src.analytics import (
    plot_habit_time_series,
    list_habits,
    habits_by_periodicity,
    longest_run_streak_for_habit,
    longest_run_streak_all,
    weekly_cigarettes_avoided_and_money_saved,
)
import random


def generate_prior_data(habit_name, initial_value=None):
    """
    Generate 28 days of prior data for a given habit name.
    Used to pre-populate time series for new habits.
    """
    if habit_name == "Cigarettes Smoked":
        start = initial_value if initial_value is not None else 5
        return [max(0, start - i // 4 + random.choice([0, 0, 1])) for i in range(28)]
    elif habit_name == "Nicotine Gum Used":
        start = initial_value if initial_value is not None else 3
        return [max(0, start - i // 5 + random.choice([0, 0, 1])) for i in range(28)]
    elif habit_name == "Sport":
        return [1 if i % 3 == 0 else random.choice([0, 1]) for i in range(28)]
    elif habit_name == "Meditation Time":
        return [1 if random.random() < 0.7 else 0 for i in range(28)]
    elif habit_name == "Specialist Appointment":
        days = [0] * 28
        days[random.randint(0, 27)] = 1
        return days
    else:
        return [0] * 28


def setup_initial_consumption(tracker: HabitTracker):
    """
    Prompt the user for initial daily values for cigarettes and gum.
    Create habits with initial_value attached.
    """
    print("=== Welcome to Quit Smoking Coach ===")
    habits_to_ask = [
        ("Cigarettes Smoked", "Reduce smoking habit"),
        ("Nicotine Gum Used", "Track nicotine gum usage"),
    ]

    initial_values = {}
    # Use actual dates for keys, not integer indices
    for name, desc in habits_to_ask:
        while True:
            try:
                value = int(input(f"How many {name} per day? "))
                break
            except ValueError:
                print("Please enter a valid number.")

        habit = Habit(name, desc, "daily", "elimination")
        habit.initial_value = value  # store the initial consumption
        today = __import__("datetime").date.today()
        habit.records = {
            today - __import__("datetime").timedelta(days=28 - i): v
            for i, v in enumerate(generate_prior_data(name, initial_value=value))
        }
        tracker.add_habit(habit)
        initial_values[name] = value

    return initial_values


def show_dashboard(tracker: HabitTracker):
    print("\nYour habits:")
    for habit in tracker.habits:
        print(f"- {habit.name} ({habit.periodicity}), records={len(habit.records)}")


def show_reduction_plans(tracker: HabitTracker):
    for habit in tracker.habits:
        if hasattr(habit, "plan") and habit.plan:
            print(f"Plan for {habit.name}:")
            print(", ".join(str(v) for v in habit.plan))


def log_habit_values(tracker: HabitTracker):
    for habit in tracker.habits:
        try:
            value = int(input(f"Enter today's value for {habit.name}: "))
            tracker.log_habit(habit.name, value)
        except ValueError:
            print("Invalid input. Skipping.")


def add_habit(tracker: HabitTracker):
    name = input("Habit name: ")
    desc = input("Description: ")
    periodicity = input("Periodicity (daily/weekly/monthly): ")
    type_ = input("Type (elimination/establishment): ")
    tracker.add_habit(Habit(name, desc, periodicity, type_))
    print(f"Habit '{name}' added!")


def remove_habit(tracker: HabitTracker):
    name = input("Habit name to remove: ")
    tracker.remove_habit(name)
    print(f"Habit '{name}' removed if existed.")


def modify_habit(tracker: HabitTracker):
    old_name = input("Name of habit to modify: ")
    new_name = input("New name (leave blank to keep): ") or None
    new_desc = input("New description (leave blank to keep): ") or None
    new_periodicity = (
        input("New periodicity (daily/weekly/monthly, leave blank to keep): ") or None
    )
    new_type = (
        input("New type (elimination/establishment, leave blank to keep): ") or None
    )
    tracker.modify_habit(old_name, new_name, new_desc, new_periodicity, new_type)
    print(f"Habit '{old_name}' modified if existed.")


def show_analytics(tracker: HabitTracker):
    print("\nTracked habits:", list_habits(tracker))
    for period in ["daily", "weekly", "monthly"]:
        print(f"{period.capitalize()} habits:", habits_by_periodicity(tracker, period))
    print("Longest streak across all habits:", longest_run_streak_all(tracker))
    for habit in tracker.habits:
        print(f"Longest streak for {habit.name}: {longest_run_streak_for_habit(habit)}")
        plot_habit_time_series(habit)
    print("\n--- Weekly Motivation ---")
    weekly_cigarettes_avoided_and_money_saved(tracker)
