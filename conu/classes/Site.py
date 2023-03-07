from dataclasses import dataclass


@dataclass
class Site:
    id: int
    name: str
    address: str
    suburb: str
