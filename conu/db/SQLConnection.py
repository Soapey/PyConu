import pyodbc
from conu.helpers import read_config_file


class SQLServerConnection:

    def __init__(self, connection_string: str = None):

        if not connection_string:
            config = read_config_file()
            driver = config["SQLServerSettings"]["driver"]
            server = config["SQLServerSettings"]["server"]
            database = config["SQLServerSettings"]["development_database_name"]
            username = config["SQLServerSettings"]["username"]
            password = config["SQLServerSettings"]["password"]
            connection_string = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"

        self.connection_string = connection_string

    def __enter__(self):
        """Open the connection to the SQL Server database and return a cursor.

        Returns:
            cursor: A cursor object for executing SQL commands on the database.

        Raises:
            pyodbc.Error: If there was an error connecting to the database.
        """
        try:
            self.connection = pyodbc.connect(self.connection_string)
            self.cursor = self.connection.cursor()
            return self.cursor
        except pyodbc.Error as e:
            raise e

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Commit the changes and close the connection to the SQL Server database.

        Raises:
            pyodbc.Error: If there was an error committing the changes to the database.
        """
        try:
            self.connection.commit()
        except pyodbc.Error as e:
            self.connection.rollback()
            raise e
        finally:
            self.cursor.close()
            self.connection.close()
