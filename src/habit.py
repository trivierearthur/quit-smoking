import datetime


class Habit:
    def __init__(self, name, description, periodicity, type_, created=None):
        self.name = name
        self.description = description
        self.periodicity = periodicity
        self.type = type_  # elimination/establishment
        self.created = created or datetime.datetime.now()
        self.records = {}  # date -> value
        self.plan = []  # reduction plan
        self.time_series = {}  # last 28 days

    def log(self, value, date=None):
        if date is None:
            date = datetime.date.today()
        self.records[date] = value
        self.time_series[date] = value

    def init_time_series(self, data):
        today = datetime.date.today()
        for i, value in enumerate(data):
            day = today - datetime.timedelta(days=28 - i)
            self.records[day] = value
            self.time_series[day] = value
