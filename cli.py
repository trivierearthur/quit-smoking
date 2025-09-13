from tracker import HabitTracker
from habit import Habit
from analytics import (
    plot_habit_time_series,
    list_habits,
    habits_by_periodicity,
    longest_streak,
    longest_streak_all,
)
import random


def generate_prior_data(habit_name):
    if habit_name == "Cigarettes Smoked":
        start = 5
        return [max(0, start - i // 4 + random.choice([0, 0, 1])) for i in range(28)]
    elif habit_name == "Nicotine Gum Used":
        start = 3
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


def setup_initial_consumption():
    print("=== Welcome to Quit Smoking Coach ===")
    habits_to_ask = ["Cigarettes Smoked", "Nicotine Gum Used"]
    initial_values = {}
    for name in habits_to_ask:
        while True:
            try:
                value = int(input(f"How many {name.lower()} per day? "))
                initial_values[name] = value
                break
            except ValueError:
                print("Please enter a valid number.")
    return initial_values


# Dashboard, logging, add/remove/modify habits, show reduction plan, analytics
def show_dashboard(tracker: HabitTracker):
    print("\nYour habits:")
    for habit in tracker.habits:
        print(f"- {habit.name} ({habit.periodicity}), records={len(habit.records)}")


def show_reduction_plans(tracker: HabitTracker):
    for habit in tracker.habits:
        print(f"\nPlan for {habit.name}:")
        if habit.plan:
            print(", ".join(str(x) for x in habit.plan[:7]) + " ...")
        else:
            print("No plan set.")


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
    print("Longest streak across all habits:", longest_streak_all(tracker))
    for habit in tracker.habits:
        print(f"Longest streak for {habit.name}: {longest_streak(habit)}")
        plot_habit_time_series(habit)
