from dataclasses import dataclass
from datetime import datetime


@dataclass
class HabitRecordModel:
    day: str
    habit_id: int
    value: int


@dataclass
class HabitModel:
    id: int
    name: str
    description: str
    periodicity: str
    habit_type: str
    created: datetime
    records: list[HabitRecordModel]
