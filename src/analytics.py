"""
Analytics module for habit tracking and progress visualization.

This module implements analytical functionality for the quit-smoking habit tracker
using functional programming paradigms. It provides comprehensive analytics including:

- Streak calculations for individual habits and across all habits
- Time series visualization for habit progress over time
- Weekly progress statistics with cigarette consumption and cost analysis
- Data visualization using matplotlib for trend analysis

The module follows functional programming principles with pure functions,
immutable data structures, and functional composition using reduce() operations.
All visualization functions generate interactive charts to help users understand
their progress and maintain motivation in their quit-smoking journey.

Key Features:
- Consecutive day streak calculations
- 28-day time series plotting
- Weekly cigarette avoidance and cost savings analysis
- Progress visualization with bar charts and line graphs
"""

from dataclasses import dataclass
from functools import reduce
from datetime import date, timedelta
from typing import Optional
import matplotlib.pyplot as plt
from src.habit_manager import HabitManager, Habit
from src import constants


@dataclass
class WeeklyCigaretteStats:
    """
    Data structure for weekly cigarette consumption and progress statistics.

    This immutable data class encapsulates the results of weekly cigarette
    analysis, providing a clear interface for progress tracking and cost
    calculations. Used by analytics functions to return structured data
    for both display and further processing.

    Attributes:
        avoided: Number of cigarettes avoided compared to baseline consumption
        spent: Total number of cigarettes actually consumed during the week
        money_saved: Monetary savings from avoided cigarettes (in euros)
        initial: Baseline daily cigarette consumption at start of period
        start_date: Beginning date of the analysis period
        end_date: End date of the analysis period
    """

    avoided: int
    spent: int
    money_saved: float
    initial: int
    start_date: date
    end_date: date


def longest_run_streak_for_habit(habit: Habit) -> int:
    """
    Calculate the longest consecutive streak for a single habit.

    This function implements streak calculation using functional programming
    principles with the reduce() function. It analyzes all recorded dates
    for a habit and finds the longest sequence of consecutive days with records.

    Algorithm:
    1. Sort all recorded dates chronologically
    2. Use reduce() with a streak_reducer function to traverse date pairs
    3. Check if consecutive dates differ by exactly 1 day
    4. Track current streak and maximum streak simultaneously
    5. Return the longest streak found

    Args:
        habit: Habit instance containing records dictionary with date keys

    Returns:
        Integer representing the longest consecutive day streak (0 if no records)

    Examples:
        If habit has records for: [2023-01-01, 2023-01-02, 2023-01-03, 2023-01-05]
        Returns: 3 (consecutive streak from Jan 1-3)
    """
    # Extract and sort all recorded dates chronologically
    dates = sorted(habit.records.keys())

    # Return 0 for habits with no recorded data
    if not dates:
        return 0

    def streak_reducer(acc, i):
        """
        Reducer function to calculate streaks using functional programming.

        Compares current date with previous date to determine if streak continues.
        Maintains both current streak length and maximum streak seen so far.

        Args:
            acc: Accumulator tuple (current_streak, max_streak)
            i: Current index in the dates array

        Returns:
            Updated tuple (new_current_streak, new_max_streak)
        """
        streak, max_streak = acc

        # Check if current date is exactly 1 day after previous date
        if (date.fromisoformat(dates[i]) - date.fromisoformat(dates[i - 1])).days == 1:
            streak += 1  # Continue the current streak
        else:
            streak = 1  # Reset streak (current date starts a new streak)

        # Return updated streak and maximum streak seen so far
        return streak, max(streak, max_streak)

    # Use reduce to process all date pairs, starting with streak=1, max=1
    _, max_streak = reduce(streak_reducer, range(1, len(dates)), (1, 1))
    return max_streak


def longest_run_streak_all(tracker) -> int:
    """
    Find the longest consecutive streak across all tracked habits.

    This function demonstrates functional programming composition by using
    reduce() to find the maximum streak among all habits in the tracker.
    It applies the longest_run_streak_for_habit function to each habit
    and returns the highest value found.

    Implementation uses pure functional programming:
    - No side effects or mutations
    - Composition of functions (reduce + max + longest_run_streak_for_habit)
    - Immutable data processing

    Args:
        tracker: HabitManager instance containing a list of habits

    Returns:
        Integer representing the longest streak found across all habits
        Returns 0 if no habits exist or no habits have records

    Examples:
        If tracker has habits with streaks of [5, 12, 3, 8] days
        Returns: 12 (the maximum streak across all habits)
    """
    return reduce(
        lambda acc, h: max(acc, longest_run_streak_for_habit(h)),
        tracker.habits,
        0,  # Initial value: 0 ensures we return 0 for empty habit lists
    )


def plot_habit_time_series(habit: "Habit"):
    """
    Generate and display a time series line chart for habit progress.

    Creates a comprehensive visualization showing habit values over the last
    28 days (configurable via DEFAULT_TIME_RANGE_IN_DAYS). The function builds
    a continuous timeline that includes missing days as zeros, providing a
    complete picture of habit consistency and trends.

    Chart Features:
    - Line chart with circular markers for data points
    - 28-day continuous timeline (including gaps as zeros)
    - Rotated date labels for better readability
    - Grid lines for easier value reading
    - Professional styling with blue color scheme

    Data Processing:
    1. Normalizes date keys to ensure consistent date handling
    2. Creates continuous timeline with missing days filled as 0
    3. Sorts dates chronologically for proper time series display
    4. Formats dates as YYYY-MM-DD strings for x-axis labels

    Args:
        habit: Habit instance containing records dictionary with date/value pairs

    Side Effects:
        - Displays interactive matplotlib chart window
        - Does not return any value (pure visualization function)

    Examples:
        For a habit with records: {"2023-01-01": 5, "2023-01-03": 3}
        Shows: 28-day chart with values 5, 0, 3, 0, 0... for consecutive days
    """
    today = date.today()
    n_days = constants.DEFAULT_TIME_RANGE_IN_DAYS  # Default: 28 days

    # Normalize habit.records keys to date objects for consistent processing
    # Handle both string ISO dates and date objects in the records
    records = {
        (day if isinstance(day, date) else date.fromisoformat(day)): value
        for day, value in habit.records.items()
    }

    # Build a continuous timeline including today, filling gaps with zeros
    # This ensures the chart shows a complete 28-day period even with missing data
    last_period = {
        today - timedelta(days=offset): records.get(today - timedelta(days=offset), 0)
        for offset in range(n_days)
    }

    # Sort by date ascending (chronological order) for proper time series display
    dates = sorted(last_period.keys())
    x_values = [d.strftime("%Y-%m-%d") for d in dates]  # Format dates for display
    y_values = [last_period[d] for d in dates]  # Extract corresponding values

    # Create and configure the matplotlib chart
    plt.figure(figsize=(10, 4))  # Wide format suitable for time series
    plt.plot(x_values, y_values, marker="o", color="tab:blue", linewidth=1.5)
    plt.title(f"{habit.name} - Last {n_days} Days")
    plt.xlabel("Date")
    plt.ylabel("Value")
    plt.xticks(rotation=45, ha="right")  # Rotate dates for better readability
    plt.grid(True, linestyle="--", alpha=0.5)  # Add subtle grid lines
    plt.tight_layout()  # Optimize spacing to prevent label cutoff
    plt.show()  # Display the interactive chart


def weekly_cigarettes_avoided_and_money_saved(
    habit_manager: "HabitManager",
) -> Optional[WeeklyCigaretteStats]:
    """
    Analyze the last 7 days of cigarette consumption for progress tracking.

    This function calculates comprehensive weekly statistics for cigarette smoking
    habits, focusing on progress measurement and financial impact analysis.
    It provides motivation through quantified achievements and cost savings.

    Analysis Components:
    1. Baseline Determination: Uses the highest daily consumption in the week
    2. Avoidance Calculation: Compares actual vs baseline consumption
    3. Cost Analysis: Calculates money saved based on avoided cigarettes
    4. Progress Tracking: Provides structured data for visualization

    Financial Calculations:
    - Uses constants: €10 per pack, 20 cigarettes per pack = €0.50 per cigarette
    - Money saved = avoided_cigarettes × €0.50

    Args:
        habit_manager: HabitManager instance containing all tracked habits

    Returns:
        WeeklyCigaretteStats object with progress data, or None if:
        - No cigarette habit found (ID: HABIT_CIGARETTE_SMOKED_ID)
        - No records exist for the cigarette habit
        - No records exist within the last 7 days

    Examples:
        If user smoked [10, 8, 6, 5, 7, 4, 3] cigarettes over 7 days:
        - Baseline (initial): 10 cigarettes/day
        - Total spent: 43 cigarettes
        - Total avoided: (10×7) - 43 = 27 cigarettes
        - Money saved: 27 × €0.50 = €13.50
    """
    today = date.today()
    week_ago = today - timedelta(days=6)  # Last 7 days inclusive

    # Find the specific cigarette smoking habit by its predefined ID
    # Uses generator expression with next() for efficient habit lookup
    habit = next(
        (
            h
            for h in habit_manager.habits
            if h.id == constants.HABIT_CIGARETTE_SMOKED_ID
        ),
        None,  # Default value if no cigarette habit found
    )

    # Early return if no cigarette habit exists or has no recorded data
    if not habit or not habit.records:
        return None

    # Filter records to only include the last 7 days
    # Convert string dates to date objects for proper comparison
    week_records = {
        date.fromisoformat(day): value
        for day, value in habit.records.items()
        if week_ago <= date.fromisoformat(day) <= today
    }

    # Return None if no records found within the week period
    if not week_records:
        return None

    # Determine baseline consumption (highest daily value in the period)
    # This represents the user's starting point for comparison
    sorted_dates = sorted(week_records)
    initial = max(week_records[d] for d in sorted_dates) if sorted_dates else 0

    # Calculate progress statistics using functional programming approaches
    # Avoided: sum of positive differences between baseline and actual consumption
    avoided = sum(max(0, initial - actual) for actual in week_records.values())

    # Spent: total cigarettes actually consumed during the week
    spent = sum(week_records.values())

    # Money saved: financial impact based on avoided cigarettes
    # Formula: avoided_cigarettes × (price_per_pack ÷ cigarettes_per_pack)
    money_saved = (
        avoided * constants.CIGARTETTE_PRICE_PER_PACK / constants.CIGARTETTE_PER_PACK
    )

    # Return structured statistics for further processing and display
    return WeeklyCigaretteStats(
        avoided=avoided,
        spent=spent,
        money_saved=money_saved,
        initial=initial,
        start_date=week_ago,
        end_date=today,
    )


def plot_weekly_stats(stats: WeeklyCigaretteStats) -> None:
    """
    Generate and display a bar chart visualization of weekly progress statistics.

    Creates a motivational 3-bar chart showing key weekly achievements in
    cigarette reduction efforts. Uses color psychology to reinforce positive
    and negative associations with different metrics.

    Chart Design:
    - Green bar: Cigarettes Avoided (positive achievement)
    - Blue bar: Money Saved in Euros (financial benefit)
    - Red bar: Cigarettes Smoked (consumption to reduce)

    Visual Features:
    - Color-coded bars for intuitive understanding
    - Value labels on/above bars for precise reading
    - Special formatting for monetary values (€ symbol, 2 decimal places)
    - Date range in title for temporal context
    - Compact 6x4 inch layout suitable for dashboard display

    Label Positioning Strategy:
    - Money labels: Inside bars with white text for contrast
    - Count labels: Above bars with black text for clarity
    - Automatic positioning prevents overlap and improves readability

    Args:
        stats: WeeklyCigaretteStats object containing progress data

    Side Effects:
        - Displays interactive matplotlib bar chart window
        - Does not return any value (pure visualization function)

    Examples:
        For stats with avoided=27, money_saved=13.50, spent=43:
        Shows 3 bars with heights [27, 13.50, 43] and appropriate colors/labels
    """
    # Define chart data with semantic color mapping
    labels = ["Cigarettes Avoided", "Money Saved (€)", "Cigarettes Smoked"]
    values = [stats.avoided, stats.money_saved, stats.spent]
    colors = [
        "tab:green",
        "tab:blue",
        "tab:red",
    ]  # Green=good, Blue=benefit, Red=negative

    # Create compact chart suitable for dashboard integration
    plt.figure(figsize=(6, 4))
    bars = plt.bar(labels, values, color=colors)
    plt.title(f"Your Progress ({stats.start_date} → {stats.end_date})")
    plt.ylabel("Count / Euros")

    # Add value labels to bars with context-appropriate formatting
    for i, bar in enumerate(bars):
        yval = bar.get_height()  # Get bar height for label positioning

        if labels[i] == "Money Saved (€)":
            # Special formatting for monetary values: white text inside bar
            plt.text(
                bar.get_x() + bar.get_width() / 2,  # Center horizontally
                yval * 0.05,  # Position near bottom (5% of height)
                f"{yval:.2f} €",  # Format with 2 decimals and € symbol
                ha="center",  # Horizontal alignment: center
                va="bottom",  # Vertical alignment: bottom
                color="white",  # White text for contrast against blue
                fontweight="bold",  # Bold for better visibility
            )
        else:
            # Standard formatting for count values: black text above bar
            plt.text(
                bar.get_x() + bar.get_width() / 2,  # Center horizontally
                yval + 0.5,  # Position slightly above bar
                f"{yval:.0f}",  # Format as whole number
                ha="center",  # Horizontal alignment: center
                va="bottom",  # Vertical alignment: bottom
            )

    plt.tight_layout()  # Optimize spacing to prevent label cutoff
    plt.show()  # Display the interactive chart
