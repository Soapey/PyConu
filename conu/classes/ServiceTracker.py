from dataclasses import dataclass
from datetime import date


@dataclass
class ServiceTracker:
    id: int
    item_id: int
    units_calibration_date: date
    current_units: int
    average_units_per_day: int
    service_due_units: int
    service_interval: int
