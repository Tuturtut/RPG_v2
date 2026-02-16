from dataclasses import dataclass


class Health:
    def __init__(self, current_health, max_health):
        self.current_health = current_health
        self.max_health = max_health


@dataclass
class Hunger:
    current: int
    max_val: int
    threshold: int = 3