from dataclasses import dataclass


@dataclass
class UnicodePlane:
    name: str
    abbreviation: int
    start: int
    finish: int
