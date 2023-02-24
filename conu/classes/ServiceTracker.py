from datetime import date
from conu.classes.Base import Base


class ServiceTracker(Base):
    """A class representing a service tracker for an item."""

    def __init__(
        self,
        item_id: int,
        units_calibration_date: date,
        current_units: int,
        average_units_per_day: int,
        service_due_units: int,
        service_interval: int,
        id_: int = None,
    ):
        """
        Initialize a new service tracker with an item ID, units calibration date, current units,
        average units per day, service due units, service interval, and optional ID.
        """
        super().__init__(id_)
        self.item_id = item_id
        self.units_calibration_date = units_calibration_date
        self.current_units = current_units
        self.average_units_per_day = average_units_per_day
        self.service_due_units = service_due_units
        self.service_interval = service_interval

    def __repr__(self) -> str:
        """Return a string representation of the service tracker."""
        values = ', '.join([f"{k}={v}" for k, v in self.__dict__.items()])
        return f"{self.__class__.__name__}({values})"
