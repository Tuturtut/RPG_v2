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
class ScheduledActivity:
    start: int
    end: int
    activity: str


@dataclass
class ScheduledAction:
    hour: int
    action: str
    minute: int = 0

ScheduledItem = ScheduledActivity | ScheduledAction

@dataclass
class Schedule:
    items: list[ScheduledItem] = None

    def get_actions_for_time(self, hours, minutes):
        for item in self.items:
            if isinstance(item, ScheduledAction) and item.hour == hours and item.minute == minutes:
                yield item.action

    def get_current_activity(self, hours, minutes=0):

        for item in self.items:
            if isinstance(item, ScheduledActivity) and item.start <= hours < item.end:
                return item.activity
        return None

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
    def str_time(self):
        return f"{self.hours:02d}:{self.minutes:02d}"
    
    @property
    def total_minutes(self):
        return self.days * 24 * 60 + self.hours * 60 + self.minutes

    def get_time(self):
        return self.days, self.hours, self.minutes