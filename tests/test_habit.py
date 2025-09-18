# import datetime
# from src.habit_manager import Habit


# def test_habit_initialization():
#     habit = Habit("Cigarettes Smoked", "desc", "daily", "elimination")
#     assert habit.name == "Cigarettes Smoked"
#     assert habit.description == "desc"
#     assert habit.periodicity == "daily"
#     assert habit.type == "elimination"


# def test_log_adds_record_and_time_series():
#     habit = Habit("Cigarettes Smoked", "desc", "daily", "elimination")
#     habit.log(5)
#     assert len(habit.records) == 1
#     # Check the value for today's date
#     today = datetime.date.today()
#     assert habit.records[today] == 5


# def test_log_defaults_to_today():
#     habit = Habit("Cigarettes Smoked", "desc", "daily", "elimination")
#     habit.log(3)
#     today = datetime.date.today()
#     assert today in habit.records


# def test_init_time_series_populates_28_days():
#     habit = Habit("Cigarettes Smoked", "desc", "daily", "elimination")
#     # Create 28 days of data starting from today
#     start_date = datetime.date.today() - datetime.timedelta(days=27)
#     data = [i for i in range(28)]
#     # Pass a dict with dates as keys
#     time_series = {start_date + datetime.timedelta(days=i): data[i] for i in range(28)}
#     habit.init_time_series(time_series)
#     assert len(habit.records) == 28
#     # Check the first value
#     assert habit.records[start_date] == 0
