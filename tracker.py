from habit import Habit


class HabitTracker:
    def __init__(self):
        self.habits = []

    def add_habit(self, habit: Habit):
        self.habits.append(habit)

    def remove_habit(self, habit_name):
        self.habits = [h for h in self.habits if h.name != habit_name]

    def modify_habit(
        self,
        old_name,
        new_name=None,
        new_desc=None,
        new_periodicity=None,
        new_type=None,
    ):
        habit = self.get_habit(old_name)
        if habit:
            if new_name:
                habit.name = new_name
            if new_desc:
                habit.description = new_desc
            if new_periodicity:
                habit.periodicity = new_periodicity
            if new_type:
                habit.type = new_type

    def get_habit(self, name):
        for h in self.habits:
            if h.name == name:
                return h
        return None

    def log_habit(self, habit_name, value):
        habit = self.get_habit(habit_name)
        if habit:
            habit.log(value)


def generate_reduction_plan(cigarettes, gums, days=28):
    plan = {}
    for habit_name, start_value in [
        ("Cigarettes Smoked", cigarettes),
        ("Nicotine Gum Used", gums),
    ]:
        step = start_value / days
        plan[habit_name] = [max(0, round(start_value - i * step)) for i in range(days)]
    return plan
