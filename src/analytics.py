import matplotlib.pyplot as plt
from functools import reduce


def list_habits(tracker):
    """
    Return a list of all currently tracked habit names.
    """
    return list(map(lambda h: h.name, tracker.habits))


def habits_by_periodicity(tracker, period):
    """
    Return a list of all habit names with the given periodicity (e.g., 'daily', 'weekly').
    """
    return list(
        map(lambda h: h.name, filter(lambda h: h.periodicity == period, tracker.habits))
    )


def longest_run_streak_for_habit(habit):
    """
    Return the longest run streak for a given habit (consecutive days with a record).
    """
    dates = sorted(habit.records.keys())
    if not dates:
        return 0

    def streak_reducer(acc, i):
        streak, max_streak = acc
        if (dates[i] - dates[i - 1]).days == 1:
            streak += 1
        else:
            streak = 1
        return streak, max(streak, max_streak)

    _, max_streak = reduce(streak_reducer, range(1, len(dates)), (1, 1))
    return max_streak


def longest_run_streak_all(tracker):
    """
    Return the longest run streak among all defined habits.
    """
    return reduce(
        lambda acc, h: max(acc, longest_run_streak_for_habit(h)), tracker.habits, 0
    )


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


def weekly_cigarettes_avoided_and_money_saved(
    tracker, price_per_pack=10.0, cigarettes_per_pack=20
):
    """
    Analyze how many cigarettes were avoided this week and how much money was saved.
    Assumes a habit named 'Cigarettes Smoked' exists and its plan is a list of target values per day.
    price_per_pack: price of a pack of cigarettes (default 10.0 €)
    cigarettes_per_pack: number of cigarettes in a pack (default 20)
    """
    import datetime

    today = datetime.date.today()
    week_ago = today - datetime.timedelta(days=6)
    habit = next((h for h in tracker.habits if h.name == "Cigarettes Smoked"), None)
    if not habit or not habit.records:
        print("No data for 'Cigarettes Smoked'.")
        return
    # Only consider records from the last 7 days
    week_records = {d: v for d, v in habit.records.items() if week_ago <= d <= today}
    if not week_records:
        print("No records for this week.")
        return
    # Calculate avoided cigarettes: (planned - actual) for each day, sum up
    avoided = 0
    spent = 0
    for d in sorted(week_records):
        idx = (d - min(habit.records)).days
        planned = (
            habit.plan[idx] if habit.plan and idx < len(habit.plan) else week_records[d]
        )
        actual = week_records[d]
        avoided += max(0, planned - actual)
        spent += actual
    # Money saved: avoided cigarettes / cigarettes_per_pack * price_per_pack
    money_saved = avoided / cigarettes_per_pack * price_per_pack
    print(f"In the last 7 days, you avoided {avoided} cigarettes!")
    print(f"You saved approximately {money_saved:.2f} € by not smoking.")
    print(f"You still smoked {spent} cigarettes this week.")
