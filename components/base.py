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
    direction: str


@dataclass
class ActionRequest:
    type: str
    priority: int

from dataclasses import dataclass

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