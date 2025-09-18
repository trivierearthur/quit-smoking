import matplotlib.pyplot as plt
from functools import reduce
import datetime


def list_habits(tracker):
    """Return a list of all currently tracked habit names."""
    return [h.name for h in tracker.habits]


def habits_by_periodicity(tracker, period):
    """Return a list of all habit names with the given periodicity."""
    return [h.name for h in tracker.habits if h.periodicity == period]


def longest_run_streak_for_habit(habit):
    """Return the longest run streak for a given habit (consecutive days with a record)."""
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
    """Return the longest run streak among all defined habits."""
    return reduce(
        lambda acc, h: max(acc, longest_run_streak_for_habit(h)), tracker.habits, 0
    )


def plot_habit_time_series(habit):
    """Plot last 28 days of a habit time series."""
    if not habit.time_series:
        print(f"No data for {habit.name}")
        return

    dates = list(habit.time_series.keys())
    values = list(habit.time_series.values())

    plt.figure(figsize=(8, 4))
    plt.plot(dates, values, marker="o", color="tab:blue")
    plt.title(f"{habit.name} - Last 28 Days")
    plt.xlabel("Date")
    plt.ylabel("Value")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def weekly_cigarettes_avoided_and_money_saved(
    tracker, price_per_pack=10.0, cigarettes_per_pack=20
):
    """Analyze last 7 days of Cigarettes Smoked and calculate money saved."""
    today = datetime.date.today()
    week_ago = today - datetime.timedelta(days=6)
    habit = next((h for h in tracker.habits if h.name == "Cigarettes Smoked"), None)

    if not habit or not habit.records:
        print("No data for 'Cigarettes Smoked'.")
        return

    # Only consider last 7 days
    week_records = {d: v for d, v in habit.records.items() if week_ago <= d <= today}
    if not week_records:
        print("No records for this week.")
        return

    # Use user-defined initial value if it exists, else fallback to max of first 7 records
    initial = getattr(habit, "initial_value", None)
    if initial is None:
        sorted_dates = sorted(week_records)
        initial = max(week_records[d] for d in sorted_dates[:7]) if sorted_dates else 0

    avoided = 0
    spent = 0
    for d, actual in week_records.items():
        avoided += max(0, initial - actual)
        spent += actual

    money_saved = avoided * price_per_pack / cigarettes_per_pack

    print(
        f"\nIn the last 7 days, you avoided {avoided} cigarettes compared to your initial consumption of {initial} per day!"
    )
    print(f"You saved approximately {money_saved:.2f} € by not smoking.")
    print(f"You still smoked {spent} cigarettes this week.")

    # Bar chart
    labels = ["Cigarettes Avoided", "Money Saved (€)", "Cigarettes Smoked"]
    values = [avoided, money_saved, spent]
    colors = ["tab:green", "tab:blue", "tab:red"]

    plt.figure(figsize=(6, 4))
    bars = plt.bar(labels, values, color=colors)
    plt.title("Your Progress This Week")
    plt.ylabel("Count / Euros")

    for i, bar in enumerate(bars):
        yval = bar.get_height()
        if labels[i] == "Money Saved (€)":
            # put label inside the bar for visibility
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                yval * 0.05,
                f"{yval:.2f} €",
                ha="center",
                va="bottom",
                color="white",
                fontweight="bold",
            )
        else:
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                yval + 0.5,
                f"{yval:.0f}",
                ha="center",
                va="bottom",
            )

    plt.tight_layout()
    plt.show()
