from src.tracker import generate_reduction_plan
from src.habit import Habit
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
from src.persistence import init_db, save_habit, load_tracker
from src.constants import PREDEFINED_HABITS


def main():
    init_db()
    tracker = load_tracker()

    # Always ask initial consumption for cigarettes & gums at startup
    initial_values = setup_initial_consumption(tracker)
    if initial_values is None:
        print("Error: Initial consumption values not provided. Exiting.")
        return

    if not tracker.habits:
        # Initialize predefined habits with realistic prior data
        for h in PREDEFINED_HABITS:
            habit = Habit(h["name"], h["description"], h["periodicity"], h["type_"])
            # Only use user input for cigarettes and gums
            if habit.name in ("Cigarettes Smoked", "Nicotine Gum Used"):
                prior_data = generate_prior_data(
                    habit.name, initial_value=initial_values[habit.name]
                )
            else:
                prior_data = generate_prior_data(habit.name)
            habit.init_time_series(prior_data)
            tracker.add_habit(habit)

        plans = generate_reduction_plan(
            initial_values["Cigarettes Smoked"], initial_values["Nicotine Gum Used"]
        )
        for habit in tracker.habits:
            if habit.name in plans:
                habit.plan = plans[habit.name]
            save_habit(habit)  # persist in DB

    while True:
        print("\n=== Quit Smoking Coach ===")
        print("1) Show dashboard (list habits)")
        print("2) Log today's values")
        print("3) Show reduction plans")
        print("4) Analytics")
        print("5) Add habit")
        print("6) Remove habit")
        print("7) Modify habit")
        print("8) Exit")

        choice = input("\nChoice: ")
        if choice == "1":
            show_dashboard(tracker)
        elif choice == "2":
            log_habit_values(tracker)
            for habit in tracker.habits:
                save_habit(habit)
        elif choice == "3":
            show_reduction_plans(tracker)
        elif choice == "4":
            show_analytics(tracker)
        elif choice == "5":
            add_habit(tracker)
            for habit in tracker.habits:
                save_habit(habit)
        elif choice == "6":
            remove_habit(tracker)
            for habit in tracker.habits:
                save_habit(habit)
        elif choice == "7":
            modify_habit(tracker)
            for habit in tracker.habits:
                save_habit(habit)
        elif choice == "8":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()
