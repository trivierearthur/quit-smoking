from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

from src import analytics, constants
from src.habit_manager import Habit, HabitManager
from src.models import HabitModel, HabitRecordModel


def test_longest_run_streak_all():
    # Arrange
    mock_db = MagicMock()
    habit_manager = HabitManager(mock_db)

    now = datetime.now()

    habit_manager.habits = [
        Habit(
            HabitModel(
                i + 1,
                "Cigarettes Smoked",
                "Number of cigarettes smoked daily",
                constants.PERIODICITY_DAILY,
                constants.HABIT_TYPE_ESTABLISHMENT,
                now,
                [HabitRecordModel(now.date().isoformat(), i + 1, 5)],
            )
        )
        for i in range(10)
    ]

    # Act
    longest_run_streak_all = analytics.longest_run_streak_all(habit_manager)

    # Assert
    assert longest_run_streak_all == 1


def test_longest_run_streak_for_habit():
    # Arrange

    now = datetime.now()
    habit = Habit(
        HabitModel(
            1,
            "Cigarettes Smoked",
            "Number of cigarettes smoked daily",
            constants.PERIODICITY_DAILY,
            constants.HABIT_TYPE_ESTABLISHMENT,
            now,
            [HabitRecordModel(now.date().isoformat(), 1, 5)],
        )
    )

    # Act
    longest_run_streak_all = analytics.longest_run_streak_for_habit(habit)

    # Assert
    assert longest_run_streak_all == 1


def test_plot_habit_time_series():
    now = datetime.now()
    habit = Habit(
        HabitModel(
            1,
            "Cigarettes Smoked",
            "Number of cigarettes smoked daily",
            constants.PERIODICITY_DAILY,
            constants.HABIT_TYPE_ESTABLISHMENT,
            now,
            [HabitRecordModel(now.date().isoformat(), 1, 5)],
        )
    )

    with patch("matplotlib.pyplot.plot") as mock_plot, patch(
        "matplotlib.pyplot.show"
    ) as mock_show:

        analytics.plot_habit_time_series(habit)

        args, _kwargs = mock_plot.call_args

        x_values = args[0]
        y_values = args[1]

        assert len(x_values) == constants.DEFAULT_TIME_RANGE_IN_DAYS
        assert len(y_values) == constants.DEFAULT_TIME_RANGE_IN_DAYS

        mock_plot.assert_called_once()
        mock_show.assert_called_once()


def test_weekly_cigarettes_avoided_and_money_saved():
    now = datetime.now()
    # Setup a habit with 7 days of decreasing values
    records = [
        HabitRecordModel(
            (now.date() - timedelta(days=i)).isoformat(), 1, 10 - i  # 10, 9, ..., 4
        )
        for i in range(7)
    ]
    habit = Habit(
        HabitModel(
            1,
            "Cigarettes Smoked",
            "Number of cigarettes smoked daily",
            constants.PERIODICITY_DAILY,
            constants.HABIT_TYPE_ELIMINATION,
            now,
            records,
        )
    )
    mock_db = MagicMock()
    habit_manager = HabitManager(mock_db)
    habit_manager.habits = [habit]

    stats = analytics.weekly_cigarettes_avoided_and_money_saved(habit_manager)

    assert stats is not None
    assert stats.avoided >= 0
    assert stats.spent == sum(10 - i for i in range(7))
    assert stats.initial == 10
    assert stats.start_date < stats.end_date
