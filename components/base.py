from dataclasses import dataclass

class Area:
    pass

class Delete:
    pass

@dataclass
class Position:
    location_name: str
    at_entity: any = None

@dataclass
class Movement:
    direction: str


@dataclass
class ActionRequest:
    type: str
    priority: int

