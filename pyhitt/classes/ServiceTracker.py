from datetime import date

class ServiceTracker:
    """
    Represents a service tracker for an item with various attributes.

    Attributes:
        id (int): The unique identifier for the service tracker.
        item_id (int): The unique identifier for the item being tracked.
        units_calibration_date (date): The date of the most recent calibration of the item.
        current_units (int): The current units of the item.
        average_units_per_day (int): The average units per day of the item.
        service_due_units (int): The number of units at which the next service is due.
        service_interval (int): The interval between services, in units.
    """

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
        Initializes a new instance of the ServiceTracker class with the specified attributes.

        Parameters:
            item_id (int): The unique identifier for the item being tracked.
            units_calibration_date (date): The date of the most recent calibration of the item.
            current_units (int): The current units of the item.
            average_units_per_day (int): The average units per day of the item.
            service_due_units (int): The number of units at which the next service is due.
            service_interval (int): The interval between services, in units.
            id_ (int, optional): The unique identifier for the service tracker.
        """
        self.id = id_
        self.item_id = item_id
        self.units_calibration_date = units_calibration_date
        self.current_units = current_units
        self.average_units_per_day = average_units_per_day
        self.service_due_units = service_due_units
        self.service_interval = service_interval
