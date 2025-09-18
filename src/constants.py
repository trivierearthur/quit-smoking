HABIT_TYPE_ELIMINATION = "ELIMINATION"
HABIT_TYPE_ESTABLISHMENT = "ESTABLISHMENT"

PERIODICITY_DAILY = "DAILY"
PERIODICITY_WEEKLY = "WEEKLY"
PERIODICITY_MONTHLY = "MONTHLY"

HABIT_CIGARETTE_SMOKED_ID = 1
HABIT_NICOTINE_GUM_USED_ID = 2
HABIT_SPECIALIST_APPOINTMENT_ID = 3
HABIT_SPORT_HABIT_ID = 4
HABIT_MEDITATION_TIME_ID = 5


DEFAULT_HABITS = [
    (
        HABIT_CIGARETTE_SMOKED_ID,
        "Cigarettes Smoked",
        "Number of cigarettes smoked",
        PERIODICITY_DAILY,
        HABIT_TYPE_ELIMINATION,
    ),
    (
        HABIT_NICOTINE_GUM_USED_ID,
        "Nicotine Gum Used",
        "Number of gums used",
        PERIODICITY_DAILY,
        HABIT_TYPE_ELIMINATION,
    ),
    (
        HABIT_MEDITATION_TIME_ID,
        "Meditation Time",
        "Spend time meditating",
        PERIODICITY_DAILY,
        HABIT_TYPE_ESTABLISHMENT,
    ),
    (
        HABIT_SPORT_HABIT_ID,
        "Sport",
        "Engage in physical activity",
        PERIODICITY_WEEKLY,
        HABIT_TYPE_ESTABLISHMENT,
    ),
    (
        HABIT_SPECIALIST_APPOINTMENT_ID,
        "Specialist Appointment",
        "Schedule and attend appointments",
        PERIODICITY_MONTHLY,
        HABIT_TYPE_ESTABLISHMENT,
    ),
]

DEFAULT_TIME_RANGE_IN_DAYS = 28

CIGARTETTE_PRICE_PER_PACK = 10
CIGARTETTE_PER_PACK = 20
