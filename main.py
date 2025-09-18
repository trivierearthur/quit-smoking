from src.db import Database
from src.habit_manager import HabitManager
from src import cli, constants


if __name__ == "__main__":

    with Database() as db:
        habit_manager = HabitManager(db)
        habit_manager.load_habits()

        if habit_manager.has_no_elimination_daily_logs():
            cli.log_values(habit_manager, constants.HABIT_TYPE_ELIMINATION)

        cli.show_menu(habit_manager)

    print("Goodbye!")
