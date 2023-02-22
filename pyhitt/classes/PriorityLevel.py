class PriorityLevel:
    """
    Represents a PriorityLevel with various attributes such as ID, name, and the number of days until it becomes overdue.
    This is assigned to a WorkOrder Item and represents the urgency of it to be completed.

    Attributes:
        id (int): The unique identifier for the task.
        name (str): The name of the task.
        days_until_overdue (int): The number of days until the task becomes overdue.
    """

    def __init__(self, name: str, days_until_overdue: int, id_: int = None):
        """
        Initializes a new instance of the Task class with the specified attributes.

        Parameters:
            name (str): The name of the task.
            days_until_overdue (int): The number of days until the task becomes overdue.
            id_ (int, optional): The unique identifier for the task.
        """
        self.id = id_
        self.name = name
        self.days_until_overdue = days_until_overdue
