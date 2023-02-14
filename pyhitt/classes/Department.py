from pyhitt.db.SQLConnection import SQLConnection

class Department:
    """A class that represents a Department entity in a database.

    Attributes:
        id (int): The id of the department.
        name (str): The name of the department.
    """

    def __init__(self, id_: int, name: str):
        """The constructor for the Department class.

        Args:
            id_ (int): The id of the department.
            name (str): The name of the department.
        """
        self.id = id_
        self.name = name

    def save_department(self, new_name: str = None):
        """Saves a department to the database.

        Args:
            new_name (str, optional): If provided, updates the name of the department in the database.

        Raises:
            Exception: If an error occurs while saving the department.
        """
        with SQLConnection("<connection_string>") as cursor:
            try:
                if new_name:
                    cursor.execute("UPDATE departments SET name='{}' WHERE id={}".format(new_name, self.id))
                else:
                    cursor.execute("INSERT INTO departments (id, name) VALUES ({}, '{}')".format(self.id, self.name))
            except Exception as error:
                print("Error saving department: {}".format(error))
                cursor.rollback()

    def read_department(self):
        """Reads a department from the database.

        Returns:
            object: The department data if found, None otherwise.

        Raises:
            Exception: If an error occurs while reading the department.
        """
        with SQLConnection("<connection_string>") as cursor:
            try:
                cursor.execute("SELECT * FROM departments WHERE id={}".format(self.id))
                return cursor.fetchone()
            except Exception as error:
                print("Error reading department: {}".format(error))
                cursor.rollback()

    def delete_department(self):
        """Deletes a department from the database.

        Raises:
            Exception: If an error occurs while deleting the department.
        """
        with SQLConnection("<connection_string>") as cursor:
            try:
                cursor.execute("DELETE FROM departments WHERE id={}".format(self.id))
            except Exception as error:
                print("Error deleting department: {}".format(error))
                cursor.rollback()