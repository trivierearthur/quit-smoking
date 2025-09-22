from typing import Callable, Dict, Tuple
from src import analytics, utils
from src.habit_manager import HabitManager
from src import constants


def print_header(title: str):
    print("\n" + title)
    print("-" * len(title))


def show_dashboard(habit_manager: HabitManager):
    print_header("Dashboard")

    for habit in habit_manager.habits:
        print(
            f"• {habit.name} ({habit.periodicity}), today={habit_manager.get_today_habit_value(habit.id)}, total={len(habit.records)}"
        )


def print_habits_by_priority(habit_manager: HabitManager):
    print("\nTracked habits by periodicity:")
    for periodicity in [
        constants.PERIODICITY_DAILY,
        constants.PERIODICITY_WEEKLY,
        constants.PERIODICITY_MONTHLY,
    ]:
        print(
            f"{periodicity} habits:",
            " | ".join(
                [h.name for h in habit_manager.habits if h.periodicity == periodicity]
            ),
        )


def show_analytics(habit_manager: HabitManager):
    print_header("Analytics")

    # Tracked habits by periodicity
    print_habits_by_priority(habit_manager)

    # Longest streak all habits
    print(
        "\nLongest streak across all habits:",
        analytics.longest_run_streak_all(habit_manager),
    )

    for habit in habit_manager.habits:
        # Longest streak per habit
        print(
            f"Longest streak for {habit.name}: {analytics.longest_run_streak_for_habit(habit)}"
        )

        # Plot habit
        analytics.plot_habit_time_series(habit)

    weekly_stats = analytics.weekly_cigarettes_avoided_and_money_saved(habit_manager)

    if weekly_stats:
        print("\n--- Weekly Stats ---")
        print(
            f"In the last 7 days ({weekly_stats.start_date} → {weekly_stats.end_date}), "
            f"you avoided {weekly_stats.avoided} cigarettes vs {weekly_stats.initial}/day baseline."
        )
        print(f"Money saved: {weekly_stats.money_saved:.2f} €")
        print(f"Still smoked: {weekly_stats.spent}")
        analytics.plot_weekly_stats(weekly_stats)
    else:
        print("No data for 'Cigarettes Smoked'.")


def show_reduction_plan(habit_manager: HabitManager):
    print_header("Show reduction plans")

    plan = {}
    for habit in [
        h
        for h in habit_manager.habits
        if h.habit_type == constants.HABIT_TYPE_ELIMINATION
    ]:
        today_record = habit_manager.get_today_habit_value(habit.id)
        step = today_record / constants.DEFAULT_TIME_RANGE_IN_DAYS
        plan[habit.name] = [
            max(0, round(today_record - i * step))
            for i in range(constants.DEFAULT_TIME_RANGE_IN_DAYS)
        ]
        print(f"Plan for {habit.name}:")
        print(", ".join(str(v) for v in plan[habit.name]))
        print()


def log_values(habit_manager: HabitManager, habit_type: str | None = None):
    print_header("Complete today habits")

    for habit in [
        h
        for h in habit_manager.habits
        if habit_type is None or h.habit_type == habit_type
    ]:
        try:
            input_value = input(f"Enter today's value for {habit.name}: ")
            habit_manager.log_today_habit(habit.id, int(input_value))
        except ValueError:
            print("Invalid input. Skipping.")


def add_habit(habit_manager: HabitManager):
    print_header("Add habit")

    name = input("Habit name: ").strip()
    desc = input("Description: ").strip()
    periodicity = utils.input_select(
        "Periodicity: ",
        [
            constants.PERIODICITY_DAILY,
            constants.PERIODICITY_WEEKLY,
            constants.PERIODICITY_MONTHLY,
        ],
    )
    habit_type = utils.input_select(
        "Type: ",
        [constants.HABIT_TYPE_ELIMINATION, constants.HABIT_TYPE_ESTABLISHMENT],
    )
    habit_manager.add_habit(name, desc, periodicity, habit_type)
    print(f"\nHabit '{name}' added!")


def delete_habit(habit_manager: HabitManager):
    print_header("Delete habit")

    selected_habit_name = utils.input_select(
        "Habit name to delete: ",
        [h.name for h in habit_manager.habits],
    )

    habit_manager.remove_habit(selected_habit_name)
    print(f"\nHabit '{selected_habit_name}' deleted!")


def update_habit(habit_manager: HabitManager):
    print_header("Update habit")

    selected_habit_name = utils.input_select(
        "Habit name to update: ",
        [h.name for h in habit_manager.habits],
    )

    new_name = input("Name: ")
    desc = input("Description: ")

    periodicity = utils.input_select(
        "Periodicity: ",
        [
            constants.PERIODICITY_DAILY,
            constants.PERIODICITY_WEEKLY,
            constants.PERIODICITY_MONTHLY,
        ],
    )

    habit_type = utils.input_select(
        "Type: ",
        [constants.HABIT_TYPE_ELIMINATION, constants.HABIT_TYPE_ESTABLISHMENT],
    )

    habit_manager.update_habit(
        selected_habit_name, new_name, desc, periodicity, habit_type
    )
    print(f"\nHabit '{selected_habit_name}' updated!")


def exit_app(_: HabitManager):
    print("\nGoodbye!")
    raise SystemExit


MENU_ACTIONS: Dict[str, Tuple[str, Callable[[HabitManager], None]]] = {
    "1": ("Dashboard (list habits)", show_dashboard),
    "2": ("Log today habits", log_values),
    "3": ("Show reduction plans", show_reduction_plan),
    "4": ("Show analytics", show_analytics),
    "5": ("Add habit", add_habit),
    "6": ("Delete habit", delete_habit),
    "7": ("Update habit", update_habit),
    "8": ("Exit", exit_app),
}


def show_menu(habit_manager: HabitManager):
    print("\n=== Quit Smoking Coach ===")

    try:
        while True:
            print("\nMenu:\n")
            for key, (label, _) in MENU_ACTIONS.items():
                print(f"{key}. {label}")

            print()
            choice = input("Select menu option: ").strip()
            action = MENU_ACTIONS.get(choice)
            if action:
                _, func = action
                func(habit_manager)
            else:
                print()
                print("Invalid option!")

    except (KeyboardInterrupt, SystemExit):
        print("\nExiting. Goodbye!")
