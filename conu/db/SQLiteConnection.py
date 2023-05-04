import sqlite3
from conu.helpers import read_config_file, sharepoint_path


class SQLiteConnection:
    """
    A context manager that provides a connection to a SQLite database.

    Usage:
    with SQLiteConnection() as cursor:
        cursor.execute("SELECT * FROM my_table")
        rows = cursor.fetchall()

    If a file path is provided, the connection is made to that file. Otherwise,
    the configuration file is read to determine the database directory and the
    connection is made to a default database file within that directory.
    """

    def __init__(self, file_path: str = None) -> None:
        """
        Initializes a new instance of the SQLiteConnection class.

        Parameters:
        file_path (Optional[str]): The path to the SQLite database file.
                                   If not provided, the default file path is used.
        """
        if not file_path:

            # Read the configuration file to get the database directory
            config = read_config_file()

            # Create the default file path within the database directory
            self.file_path = sharepoint_path(config["SQLiteSettings"]["database_file"])

        else:
            self.file_path = file_path

    def __enter__(self):
        """
        Enters the context of the SQLiteConnection object.

        Returns:
        A cursor object that can be used to execute SQL queries.
        """
        # Open a connection to the SQLite database
        self.connection = sqlite3.connect(self.file_path)
        # Enable foreign key constraints
        cursor = self.connection.cursor()
        cursor.execute("pragma foreign_keys = on;")
        # Return the cursor object
        return cursor

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exits the context of the SQLiteConnection object.

        Commits any changes made to the database. If an exception occurred during
        execution of the code block, rolls back the changes instead.

        Parameters:
        exc_type: The type of exception that occurred, if any.
        exc_value: The value of the exception that occurred, if any.
        traceback: The traceback object for the exception that occurred, if any.
        """
        try:
            self.connection.commit()
        except Exception:
            self.connection.rollback()
        finally:
            self.connection.close()
