from dataclasses import dataclass

@dataclass
class Health:
    current: int = 20
    max_val: int = 20


@dataclass
class Hunger:
    current: int
    max_val: int
    threshold: int = 3

class Dead:
    pass

@dataclass
class Mindset:
    trait: str