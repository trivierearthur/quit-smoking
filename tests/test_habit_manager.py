"""
Test suite for habit_manager module.

This module contains unit tests for the HabitManager class functionality in the
quit-smoking habit tracker application. It tests core habit management operations
including:
- Adding new habits to the system
- Updating existing habit properties
- Removing habits from tracking
- Database interaction validation

The tests use mock database objects to isolate the habit management logic
from database implementation details and ensure reliable, fast unit testing.
"""

from datetime import datetime
from unittest.mock import MagicMock

from src import constants
from src.habit_manager import Habit, HabitManager
from src.models import HabitModel


def test_add_habit():
    """
    Test the add_habit functionality of HabitManager.

    This test verifies that the HabitManager correctly adds a new habit to the
    system and interacts properly with the database layer. It validates both
    the in-memory habit list updates and the database method calls.

    Test scenario:
    - Mock database to return a new HabitModel when add_habit is called
    - Create HabitManager with empty habit list
    - Add a new cigarette tracking habit
    - Verify habit was added to manager's habit list
    - Verify database add_habit method was called with correct parameters
    """
    # Arrange - Set up mock database with expected behavior
    mock_db = MagicMock()
    # Configure mock to return a HabitModel when add_habit is called
    mock_db.add_habit.side_effect = (
        lambda name, desc, periodicity, habit_type: HabitModel(
            1, name, desc, periodicity, habit_type, datetime.now(), []
        )
    )

    # Create habit manager with empty habit list
    habit_manager = HabitManager(mock_db)
    habit_manager.habits = []

    # Define test habit properties
    test_name = "Cigarettes Smoked"
    test_desc = "Number of cigarettes smoked daily"
    test_periodicity = constants.PERIODICITY_DAILY
    test_type = constants.HABIT_TYPE_ELIMINATION

    # Act - Add the new habit to the manager
    habit_manager.add_habit(test_name, test_desc, test_periodicity, test_type)

    # Assert - Verify habit was added correctly
    assert len(habit_manager.habits) == 1
    assert habit_manager.habits[0].name == test_name

    # Verify database interaction
    mock_db.add_habit.assert_called_with(
        test_name, test_desc, test_periodicity, test_type
    )


def test_update_habit():
    """
    Test the update_habit functionality of HabitManager.

    This test verifies that the HabitManager correctly updates an existing habit's
    properties and synchronizes changes with the database. It tests the complete
    update workflow including parameter changes and database interaction.

    Test scenario:
    - Create a HabitManager with one existing habit
    - Update all properties of the habit (name, description, periodicity, type)
    - Verify the habit's properties were updated in memory
    - Verify the database update_habit method was called with correct parameters
    """
    # Arrange - Set up mock database and habit manager
    mock_db = MagicMock()

    habit_manager = HabitManager(mock_db)

    # Create an existing habit with initial properties
    existing_habit = Habit(
        HabitModel(
            1,  # Habit ID
            "Cigarettes Smoked",
            "Number of cigarettes smoked daily",
            constants.PERIODICITY_DAILY,
            constants.HABIT_TYPE_ESTABLISHMENT,
            datetime.now(),
            [],
        )
    )

    # Add existing habit to manager
    habit_manager.habits = [existing_habit]

    # Define new properties for the habit update
    new_name = "Cigarettes Smoked Updated"
    new_desc = "Number of cigarettes smoked monthly"
    new_periodicity = constants.PERIODICITY_MONTHLY
    new_type = constants.HABIT_TYPE_ELIMINATION

    # Act - Update the habit with new properties
    habit_manager.update_habit(
        existing_habit.name, new_name, new_desc, new_periodicity, new_type
    )

    # Assert - Verify habit properties were updated in memory
    assert len(habit_manager.habits) == 1  # Still only one habit
    assert habit_manager.habits[0].name == new_name
    assert habit_manager.habits[0].description == new_desc
    assert habit_manager.habits[0].periodicity == new_periodicity
    assert habit_manager.habits[0].habit_type == new_type

    # Verify database update was called with correct parameters
    mock_db.update_habit.assert_called_with(
        1, new_name, new_desc, new_periodicity, new_type
    )


def test_remove_habit():
    """
    Test the remove_habit functionality of HabitManager.

    This test verifies that the HabitManager correctly removes a habit from the
    system and properly calls the database deletion method. It ensures both the
    in-memory habit list is updated and the database is synchronized.

    Test scenario:
    - Create a HabitManager with one existing habit
    - Remove the habit by name
    - Verify the habit was removed from the manager's habit list
    - Verify the database delete_habit method was called with correct habit ID
    """
    # Arrange - Set up mock database and habit manager
    mock_db = MagicMock()

    habit_manager = HabitManager(mock_db)

    # Create an existing habit to be removed
    existing_habit = Habit(
        HabitModel(
            1,  # Habit ID that should be used in database deletion
            "Cigarettes Smoked",
            "Number of cigarettes smoked daily",
            constants.PERIODICITY_DAILY,
            constants.HABIT_TYPE_ESTABLISHMENT,
            datetime.now(),
            [],
        )
    )

    # Add existing habit to manager's habit list
    habit_manager.habits = [existing_habit]

    # Act - Remove the habit by name
    habit_manager.remove_habit(existing_habit.name)

    # Assert - Verify habit was removed from memory
    assert len(habit_manager.habits) == 0  # Habit list should be empty

    # Verify database deletion was called with correct habit ID
    mock_db.delete_habit.assert_called_with(existing_habit.id)
