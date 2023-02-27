from dataclasses import dataclass


@dataclass
class PriorityLevel:
    id: int
    name: str
    days_until_overdue: int
