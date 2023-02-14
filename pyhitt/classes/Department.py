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

    def save(self):
        with SQLConnection() as cursor:
            try:
                if self.id:
                    cursor.execute(
                        "UPDATE departments SET name=? WHERE id=?",
                        (
                            self.name,
                            self.id,
                        ),
                    )
                else:
                    cursor.execute(
                        "INSERT INTO departments (id, name) VALUES (?, ?)",
                        (
                            self.id,
                            self.name,
                        ),
                    )
            except Exception as error:
                print("Error saving department: {}".format(error))
                cursor.rollback()

    def delete(self):
        """Deletes a department from the database.

        Raises:
            Exception: If an error occurs while deleting the department.
        """
        with SQLConnection() as cursor:
            try:
                cursor.execute("DELETE FROM departments WHERE id=?", (self.id,))
            except Exception as error:
                print("Error deleting department: {}".format(error))
                cursor.rollback()

    @classmethod
    def get(cls, ids: list[int] = None) -> dict:
        """
        Retrieves the id and name columns from the departments table in a SQL Server database using pyodbc.

        Args:
            ids (list[int], optional): A list of integers representing department ids to retrieve. If not provided,
                all departments will be retrieved. Defaults to None.

        Returns:
            dict: A dictionary containing the id and name columns of the departments table as key-value pairs.

        Raises:
            Exception: If an error occurs while connecting to or querying the database.
        """

        try:
            with SQLConnection() as cursor:
                if ids:
                    cursor.execute(
                        "SELECT id, name FROM departments WHERE id IN (?)",
                        (", ".join(str(i) for i in ids),),
                    )
                    return cursor.fetchall()
                else:
                    cursor.execute("SELECT id, name FROM departments")
                    return cursor.fetchall()
        except Exception as error:
            print("Error retrieving data from database: {}".format(error))

    @classmethod
    def convert_sql_to_dict(cls, tuples: list[tuple]) -> dict:
        """Converts a list of SQL result tuples to a dictionary of Department objects.

        Args:
            tuples (list[tuple]): A list of tuples containing the SQL results. Each tuple should have two values: an integer representing the department ID and a string representing the department name.

        Returns:
            dict: A dictionary where the key is the department ID and the value is a Department object with the corresponding ID and name.
        """
        return {t[0]: Department(t[0], t[1]) for t in tuples}

    @classmethod
    def write_to_table(cls, table: QTableWidget, departments) -> None:
        """
        Writes the id and name attributes of Department objects to a PyQt QTableWidget.

        Args:
            table: A QTableWidget object to write data to.
            departments: A dictionary of Department objects where the key of the dictionary is the id
                of the Department and the value of the dictionary is the Department object.

        Returns:
            None.

        Raises:
            Exception: An error occurred while writing data to the table.

        Example usage:
            table = QTableWidget()
            departments = {1: Department(1, "Accounting"), 2: Department(2, "Marketing"), 3: Department(3, "Sales")}
            write_to_table(table, departments)
        """
        try:
            # clear the table and its contents
            table.clearContents()
            table.setRowCount(0)

            # write data to table
            for department_id, department in departments.items():
                row_position = table.rowCount()
                table.insertRow(row_position)
                table.setItem(row_position, 0, QTableWidgetItem(str(department_id)))
                table.setItem(row_position, 1, QTableWidgetItem(department.name))
        except Exception as e:
            print(f"Error occurred while writing data to table: {e}")
