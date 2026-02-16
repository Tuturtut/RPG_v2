from dataclasses import dataclass, field

@dataclass
class Inventory:
    items: list = field(default_factory=list)

@dataclass
class Item:
    type: str = None

@dataclass
class Value:
    value: int

@dataclass
class TradeRequest:
    sender: any = None
    receiver: any = None
    item: str = None
    status: str = "PENDING"

@dataclass
class Service:
    type: str