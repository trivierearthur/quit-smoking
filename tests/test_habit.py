import datetime
from src.habit import Habit


def test_habit_initialization():
    # Test that a habit is initialized with correct attributes and empty data
    habit = Habit("No Smoking", "Quit smoking cigarettes", "daily", "elimination")
    assert habit.name == "No Smoking"
    assert habit.description == "Quit smoking cigarettes"
    assert habit.periodicity == "daily"
    assert habit.type == "elimination"
    assert isinstance(habit.created, datetime.datetime)
    assert habit.records == {}
    assert habit.plan == []
    assert habit.time_series == {}


def test_log_adds_record_and_time_series():
    # Test that logging a value adds it to both records and time_series for a given date
    habit = Habit("Test", "desc", "daily", "elimination")
    test_date = datetime.date(2025, 9, 13)
    habit.log(5, date=test_date)
    assert habit.records[test_date] == 5
    assert habit.time_series[test_date] == 5


def test_log_defaults_to_today(monkeypatch):
    # Test that logging without a date uses today's date
    habit = Habit("Test", "desc", "daily", "elimination")
    fake_today = datetime.date(2025, 9, 13)
    monkeypatch.setattr(
        datetime, "date", type("date", (), {"today": staticmethod(lambda: fake_today)})
    )
    habit.log(3)
    assert habit.records[fake_today] == 3
    assert habit.time_series[fake_today] == 3


def test_init_time_series_populates_28_days():
    # Test that initializing time series populates 28 days of records and time_series
    habit = Habit("Test", "desc", "daily", "elimination")
    data = list(range(1, 29))  # 28 days of data
    today = datetime.date.today()
    habit.init_time_series(data)
    for i, value in enumerate(data):
        day = today - datetime.timedelta(days=28 - i)
        assert habit.records[day] == value
        assert habit.time_series[day] == value
