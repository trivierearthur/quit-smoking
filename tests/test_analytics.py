"""
Test suite for analytics module.

This module contains unit tests for the analytics functionality of the quit-smoking
habit tracker application. It tests various analytical features including:
- Streak calculation and tracking
- Time series data visualization
- Progress statistics and metrics
- Money and cigarette consumption analytics

The tests use mocked database connections and sample habit data to verify
the correctness of analytical calculations and visualizations.
"""

from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

from src import analytics, constants
from src.habit_manager import Habit, HabitManager
from src.models import HabitModel, HabitRecordModel


def test_longest_run_streak_all():
    """
    Test the longest_run_streak_all function with multiple habits.

    This test verifies that the analytics function correctly calculates the longest
    streak across all habits in the habit manager. It creates 10 test habits with
    single records and expects a streak of 1 for all of them.

    Test scenario:
    - Create 10 habits, each with one habit record
    - Call longest_run_streak_all function
    - Verify the returned streak length is 1
    """
    # Arrange - Set up mock database and create test habit manager
    mock_db = MagicMock()
    habit_manager = HabitManager(mock_db)

    now = datetime.now()

    # Create 10 test habits with single records each
    habit_manager.habits = [
        Habit(
            HabitModel(
                i + 1,  # Unique ID for each habit
                "Cigarettes Smoked",
                "Number of cigarettes smoked daily",
                constants.PERIODICITY_DAILY,
                constants.HABIT_TYPE_ESTABLISHMENT,
                now,
                [HabitRecordModel(now.date().isoformat(), i + 1, 5)],  # Single record
            )
        )
        for i in range(10)  # Generate 10 habits
    ]

    # Act - Calculate the longest streak across all habits
    longest_run_streak_all = analytics.longest_run_streak_all(habit_manager)

    # Assert - Verify the expected streak length
    assert longest_run_streak_all == 1


def test_longest_run_streak_for_habit():
    """
    Test the longest_run_streak_for_habit function with a single habit.

    This test verifies that the analytics function correctly calculates the longest
    streak for an individual habit. It creates a single habit with one record and
    verifies the streak calculation.

    Test scenario:
    - Create a single habit with one habit record
    - Call longest_run_streak_for_habit function
    - Verify the returned streak length is 1
    """
    # Arrange - Set up test data with current timestamp
    now = datetime.now()

    # Create a single habit with one record
    habit = Habit(
        HabitModel(
            1,  # Habit ID
            "Cigarettes Smoked",
            "Number of cigarettes smoked daily",
            constants.PERIODICITY_DAILY,
            constants.HABIT_TYPE_ESTABLISHMENT,
            now,
            [
                HabitRecordModel(now.date().isoformat(), 1, 5)
            ],  # Single record with value 5
        )
    )

    # Act - Calculate the longest streak for this specific habit
    longest_run_streak_all = analytics.longest_run_streak_for_habit(habit)

    # Assert - Verify the expected streak length
    assert longest_run_streak_all == 1


def test_plot_habit_time_series():
    """
    Test the plot_habit_time_series function for data visualization.

    This test verifies that the plotting function correctly generates time series
    visualizations for habit data. It mocks matplotlib functions to test the
    plotting behavior without actually displaying charts.

    Test scenario:
    - Create a habit with one record
    - Mock matplotlib.pyplot.plot and show functions
    - Call plot_habit_time_series function
    - Verify that plot data has correct dimensions and functions are called
    """
    # Arrange - Create test habit with sample data
    now = datetime.now()
    habit = Habit(
        HabitModel(
            1,
            "Cigarettes Smoked",
            "Number of cigarettes smoked daily",
            constants.PERIODICITY_DAILY,
            constants.HABIT_TYPE_ESTABLISHMENT,
            now,
            [HabitRecordModel(now.date().isoformat(), 1, 5)],  # Single data point
        )
    )

    # Mock matplotlib functions to avoid actual plotting during tests
    with patch("matplotlib.pyplot.plot") as mock_plot, patch(
        "matplotlib.pyplot.show"
    ) as mock_show:

        # Act - Generate the time series plot
        analytics.plot_habit_time_series(habit)

        # Extract the plotted data from mock function call
        args, _kwargs = mock_plot.call_args

        x_values = args[0]  # Time axis data
        y_values = args[1]  # Habit value data

        # Assert - Verify plot data dimensions match expected time range
        assert len(x_values) == constants.DEFAULT_TIME_RANGE_IN_DAYS
        assert len(y_values) == constants.DEFAULT_TIME_RANGE_IN_DAYS

        # Verify that matplotlib functions were called exactly once
        mock_plot.assert_called_once()
        mock_show.assert_called_once()


def test_weekly_cigarettes_avoided_and_money_saved():
    """
    Test the weekly_cigarettes_avoided_and_money_saved function for progress analytics.

    This test verifies that the analytics function correctly calculates weekly
    progress statistics including cigarettes avoided, money spent, and consumption
    trends over a 7-day period.

    Test scenario:
    - Create a habit with 7 days of decreasing cigarette consumption (10 down to 4)
    - Call weekly_cigarettes_avoided_and_money_saved function
    - Verify the calculated statistics are accurate and within expected ranges
    """
    # Arrange - Set up test data with current timestamp
    now = datetime.now()

    # Setup a habit with 7 days of decreasing cigarette consumption values
    # Day 0: 10 cigarettes, Day 1: 9 cigarettes, ..., Day 6: 4 cigarettes
    records = [
        HabitRecordModel(
            (now.date() - timedelta(days=i)).isoformat(),  # Date going backwards
            1,  # Habit ID
            10 - i,  # Decreasing consumption: 10, 9, 8, 7, 6, 5, 4
        )
        for i in range(7)  # Generate 7 days of records
    ]

    # Create habit with elimination type (reducing cigarette consumption)
    habit = Habit(
        HabitModel(
            1,
            "Cigarettes Smoked",
            "Number of cigarettes smoked daily",
            constants.PERIODICITY_DAILY,
            constants.HABIT_TYPE_ELIMINATION,  # Goal is to eliminate/reduce
            now,
            records,
        )
    )

    # Set up habit manager with the test habit
    mock_db = MagicMock()
    habit_manager = HabitManager(mock_db)
    habit_manager.habits = [habit]

    # Act - Calculate weekly progress statistics
    stats = analytics.weekly_cigarettes_avoided_and_money_saved(habit_manager)

    # Assert - Verify calculated statistics are correct
    assert stats is not None  # Ensure function returns valid stats object
    assert stats.avoided >= 0  # Cigarettes avoided should be non-negative
    assert stats.spent == sum(
        10 - i for i in range(7)
    )  # Total spent: 10+9+8+7+6+5+4 = 49
    assert stats.initial == 10  # Initial consumption was 10 cigarettes
    assert stats.start_date < stats.end_date  # Date range should be valid
