"""
constants.py
This module defines application-wide constants for the Quit Smoking app.

PREDEFINED_HABITS is a list of dictionaries, each representing a habit that is tracked by default when a new user starts the app.
Each habit includes:
    - name: The display name of the habit
    - description: A short explanation of what is tracked
    - periodicity: How often the habit is tracked (daily, weekly, monthly)
    - type_: Whether the habit is an 'elimination' (reduce/quit) or 'establishment' (build/start) habit

This list is used to initialize the user's habit tracker with meaningful default habits and to provide context for analytics and planning features.
"""

PREDEFINED_HABITS = [
    {
        "name": "Cigarettes Smoked",
        "description": "Number of cigarettes smoked",
        "periodicity": "daily",
        "type_": "elimination",
    },
    {
        "name": "Nicotine Gum Used",
        "description": "Number of gums used",
        "periodicity": "daily",
        "type_": "elimination",
    },
    {
        "name": "Specialist Appointment",
        "description": "Schedule and attend appointments",
        "periodicity": "monthly",
        "type_": "establishment",
    },
    {
        "name": "Sport",
        "description": "Engage in physical activity",
        "periodicity": "weekly",
        "type_": "establishment",
    },
    {
        "name": "Meditation Time",
        "description": "Spend time meditating",
        "periodicity": "daily",
        "type_": "establishment",
    },
]
