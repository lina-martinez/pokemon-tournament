from dataclasses import dataclass
from typing import Tuple


@dataclass
class Pokemon:
    name: str
    generation: str
    type: str
    abilities: Tuple[str, ...]
    health_points: float
    attack: int
    defense: int
    speed: int