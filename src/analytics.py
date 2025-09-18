from dataclasses import dataclass
from functools import reduce
from datetime import date, timedelta
from typing import Optional
import matplotlib.pyplot as plt
from src.habit_manager import HabitManager, Habit
from src import constants


@dataclass
class WeeklyCigaretteStats:
    avoided: int
    spent: int
    money_saved: float
    initial: int
    start_date: date
    end_date: date


def longest_run_streak_for_habit(habit: Habit) -> int:
    """Return the longest run streak for a given habit (consecutive days with a record)."""
    dates = sorted(habit.records.keys())

    if not dates:
        return 0

    def streak_reducer(acc, i):
        streak, max_streak = acc
        if (date.fromisoformat(dates[i]) - date.fromisoformat(dates[i - 1])).days == 1:
            streak += 1
        else:
            streak = 1

        return streak, max(streak, max_streak)

    _, max_streak = reduce(streak_reducer, range(1, len(dates)), (1, 1))
    return max_streak


def longest_run_streak_all(tracker) -> int:
    """Return the longest run streak among all defined habits."""
    return reduce(
        lambda acc, h: max(acc, longest_run_streak_for_habit(h)), tracker.habits, 0
    )


def plot_habit_time_series(habit: "Habit"):
    """Plot last N days of a habit time series."""
    today = date.today()
    n_days = constants.DEFAULT_TIME_RANGE_IN_DAYS

    # Normalize habit.records keys to dates
    records = {
        (day if isinstance(day, date) else date.fromisoformat(day)): value
        for day, value in habit.records.items()
    }

    # Build a continuous timeline (including today)
    last_period = {
        today - timedelta(days=offset): records.get(today - timedelta(days=offset), 0)
        for offset in range(n_days)
    }

    # Sort by date ascending (chronological order)
    dates = sorted(last_period.keys())
    x_values = [d.strftime("%Y-%m-%d") for d in dates]
    y_values = [last_period[d] for d in dates]

    # Plot
    plt.figure(figsize=(10, 4))
    plt.plot(x_values, y_values, marker="o", color="tab:blue", linewidth=1.5)
    plt.title(f"{habit.name} - Last {n_days} Days")
    plt.xlabel("Date")
    plt.ylabel("Value")
    plt.xticks(rotation=45, ha="right")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()


def weekly_cigarettes_avoided_and_money_saved(
    habit_manager: "HabitManager",
) -> Optional[WeeklyCigaretteStats]:
    """Analyze last 7 days of Cigarettes Smoked and return stats."""

    today = date.today()
    week_ago = today - timedelta(days=6)

    # Get cigarette habit
    habit = next(
        (
            h
            for h in habit_manager.habits
            if h.id == constants.HABIT_CIGARETTE_SMOKED_ID
        ),
        None,
    )
    if not habit or not habit.records:
        return None

    # Filter last 7 days
    week_records = {
        date.fromisoformat(day): value
        for day, value in habit.records.items()
        if week_ago <= date.fromisoformat(day) <= today
    }
    if not week_records:
        return None

    # Determine baseline
    sorted_dates = sorted(week_records)
    initial = max(week_records[d] for d in sorted_dates) if sorted_dates else 0

    # Aggregate
    avoided = sum(max(0, initial - actual) for actual in week_records.values())
    spent = sum(week_records.values())
    money_saved = (
        avoided * constants.CIGARTETTE_PRICE_PER_PACK / constants.CIGARTETTE_PER_PACK
    )

    return WeeklyCigaretteStats(
        avoided=avoided,
        spent=spent,
        money_saved=money_saved,
        initial=initial,
        start_date=week_ago,
        end_date=today,
    )


def plot_weekly_stats(stats: WeeklyCigaretteStats) -> None:
    """Plot a summary of the weekly cigarette statistics."""
    labels = ["Cigarettes Avoided", "Money Saved (€)", "Cigarettes Smoked"]
    values = [stats.avoided, stats.money_saved, stats.spent]
    colors = ["tab:green", "tab:blue", "tab:red"]

    plt.figure(figsize=(6, 4))
    bars = plt.bar(labels, values, color=colors)
    plt.title(f"Your Progress ({stats.start_date} → {stats.end_date})")
    plt.ylabel("Count / Euros")

    for i, bar in enumerate(bars):
        yval = bar.get_height()
        if labels[i] == "Money Saved (€)":
            # Label inside the bar for better visibility
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
