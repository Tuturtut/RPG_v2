from dataclasses import dataclass


class Inventory:
    def __init__(self, items=None):
        self.items = items if items is not None else []

class TradeRequest:
    def __init__(self, sender, receiver, item):
        self.sender = sender
        self.receiver = receiver
        self.item = item
        self.status = "PENDING"

@dataclass
class Service:
    type: str