import matplotlib.pyplot as plt

list_habits = lambda tracker: [h.name for h in tracker.habits]
habits_by_periodicity = lambda tracker, period: [
    h.name for h in tracker.habits if h.periodicity == period
]


def longest_streak(habit):
    dates = sorted(habit.records.keys())
    if not dates:
        return 0
    max_streak = streak = 1
    for i in range(1, len(dates)):
        if (dates[i] - dates[i - 1]).days == 1:
            streak += 1
        else:
            streak = 1
        max_streak = max(max_streak, streak)
    return max_streak


def longest_streak_all(tracker):
    return max((longest_streak(h) for h in tracker.habits), default=0)


def plot_habit_time_series(habit):
    if not habit.time_series:
        print(f"No data for {habit.name}")
        return

    dates = list(habit.time_series.keys())
    values = list(habit.time_series.values())

    plt.figure(figsize=(8, 4))
    plt.plot(dates, values, marker="o", color="tab:blue")
    plt.title(f"{habit.name} - Last 4 Weeks")
    plt.xlabel("Date")
    plt.ylabel("Value")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
