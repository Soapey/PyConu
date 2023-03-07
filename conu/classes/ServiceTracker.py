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

    def is_due(self) -> bool:

        days_since_calibration = date.today() - self.units_calibration_date
        estimated_current_units = self.current_units + (days_since_calibration * self.average_units_per_day)
        return estimated_current_units >= self.service_due_units


