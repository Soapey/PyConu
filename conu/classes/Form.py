from dataclasses import dataclass


@dataclass
class Form:
    id: int
    name: str
    path: str