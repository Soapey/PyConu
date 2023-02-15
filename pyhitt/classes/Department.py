from pyhitt.db.SQLConnection import SQLConnection
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem


class Department:
    """A class that represents a Department entity in a database.

    Attributes:
        id (int): The id of the department.
        name (str): The name of the department.
    """

    def __init__(self, id_: int = None, name: str = None):
        """The constructor for the Department class.

        Args:
            id_ (int): The id of the department.
            name (str): The name of the department.
        """
        self.id = id_
        self.name = name
