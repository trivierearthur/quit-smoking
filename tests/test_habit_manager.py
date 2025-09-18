from unittest.mock import MagicMock

from src import constants
from src.habit_manager import Habit, HabitManager
from src.models import HabitModel


def test_add_habit():
    # Arrange
    mock_db = MagicMock()
    mock_db.add_habit.side_effect = (
        lambda name, desc, periodicity, habit_type: HabitModel(
            1, name, desc, periodicity, habit_type, None, []
        )
    )

    habit_manager = HabitManager(mock_db)
    habit_manager.habits = []

    test_name = "Cigarettes Smoked"
    test_desc = "Number of cigarettes smoked daily"
    test_periodicity = constants.PERIODICITY_DAILY
    test_type = constants.HABIT_TYPE_ELIMINATION

    # Act
    habit_manager.add_habit(test_name, test_desc, test_periodicity, test_type)

    # Assert
    assert len(habit_manager.habits) == 1
    assert habit_manager.habits[0].name == test_name

    mock_db.add_habit.assert_called_with(
        test_name, test_desc, test_periodicity, test_type
    )


def test_update_habit():
    # Arrange
    mock_db = MagicMock()

    habit_manager = HabitManager(mock_db)
    existing_habit = Habit(
        HabitModel(
            1,
            "Cigarettes Smoked",
            "Number of cigarettes smoked daily",
            constants.PERIODICITY_DAILY,
            constants.HABIT_TYPE_ESTABLISHMENT,
            None,
            {},
        )
    )

    habit_manager.habits = [existing_habit]

    new_name = "Cigarettes Smoked Updated"
    new_desc = "Number of cigarettes smoked monthly"
    new_periodicity = constants.PERIODICITY_MONTHLY
    new_type = constants.HABIT_TYPE_ELIMINATION

    # Act
    habit_manager.update_habit(
        existing_habit.name, new_name, new_desc, new_periodicity, new_type
    )

    # Assert
    assert len(habit_manager.habits) == 1
    assert habit_manager.habits[0].name == new_name
    assert habit_manager.habits[0].description == new_desc
    assert habit_manager.habits[0].periodicity == new_periodicity
    assert habit_manager.habits[0].habit_type == new_type

    mock_db.update_habit.assert_called_with(
        1, new_name, new_desc, new_periodicity, new_type
    )


def test_remove_habit():
    # Arrange
    mock_db = MagicMock()

    habit_manager = HabitManager(mock_db)
    existing_habit = Habit(
        HabitModel(
            1,
            "Cigarettes Smoked",
            "Number of cigarettes smoked daily",
            constants.PERIODICITY_DAILY,
            constants.HABIT_TYPE_ESTABLISHMENT,
            None,
            {},
        )
    )

    habit_manager.habits = [existing_habit]

    # Act
    habit_manager.remove_habit(existing_habit.name)

    # Assert
    assert len(habit_manager.habits) == 0

    mock_db.delete_habit.assert_called_with(existing_habit.id)
