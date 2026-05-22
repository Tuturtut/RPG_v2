from dataclasses import dataclass

class Area:
    pass

class Delete:
    pass

@dataclass
class Position:
    at_entity_id: any = None
    is_in_transit: bool = False
    is_held_by: any = None

@dataclass
class Exits:
    connections: dict

@dataclass
class Movement:
    target_entity_id: any

@dataclass
class Schedule:
    entries: dict = None

    def get_current_activity(self, current_hour):

        valid_hours = [
            hour
            for hour in self.entries
            if hour <= current_hour
        ]

        if not valid_hours:
            return None

        latest_hour = max(valid_hours)

        return self.entries[latest_hour]

@dataclass
class Goal:
    value: str

@dataclass
class ActionRequest:
    type: str
    priority: int

@dataclass
class GameClock:
    tick: int = 0
    minutes: int = 0
    hours: int = 8
    days: int = 1

    @property
    def is_night(self):
        return self.hours < 6 or self.hours > 20

    @property
    def time(self):
        return f"{self.hours:02d}:{self.minutes:02d}"