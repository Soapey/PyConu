import os
import sqlite3
from conu.classes.Base import Base
from conu.helpers import read_config_file


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
            database_directory = config['SQLiteSettings']['database_directory']

            # Create the default file path within the database directory
            self.file_path = os.path.join(database_directory, 'conu.sqlite')

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


def save_by_list(entities: list[Base]) -> None:
    """
    Saves a list of entities into a sqlite3 database.

    Parameters:
        entities (list): A list of entities to save into the database.
                         Each entity should be an object with attributes
                         corresponding to the columns of the database table.
    """
    if not entities:
        return None

    # Get the table name based on the entity class name
    table_name = entities[0].__class__.__name__.lower()

    with SQLiteConnection() as cur:

        # Get the column names for the entity
        columns = [attr for attr in dir(entities[0]) if not callable(getattr(entities[0], attr)) and not attr.startswith("__")]

        # If the entity has an id, update the existing row in the table. Otherwise, insert a new row into the table.
        for entity in entities:
            values = [getattr(entity, col) for col in columns]

            if entity.id:
                update_query = f"UPDATE {table_name} SET {', '.join([f'{col} = ?' for col in columns])} WHERE id = ?"
                cur.execute(update_query, (*values, entity.id))
            else:
                insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['?' for col in columns])})"
                cur.execute(insert_query, values)


def delete_by_attrs_dict(cls: type, attrs: dict) -> None:
    """
    Deletes entities from a SQLite database based on attribute-value pairs.

    Parameters:
    cls (type): The class of the entities to delete.
                The table name in the database will be the class name in lowercase.
    attrs (dict): A dictionary of attribute-value pairs to match for deleting entities.
    """
    with SQLiteConnection() as cur:

        # Get the table name based on the class name
        table_name = cls.__name__.lower()

        # Construct the SQL query to delete entities with the given attribute-value pairs
        delete_query = f"DELETE FROM {table_name} WHERE {' AND '.join(f'{attr} = ?' for attr in attrs)}"
        cur.execute(delete_query, tuple(attrs.values()))


def select_by_attrs_dict(cls: type, attrs: dict) -> dict:
    """
    Selects all entities of the given class that match the specified attribute-value pairs.

    Parameters:
        cls (type): The class of the entities to select.
        attrs (dict): A dictionary of attribute-value pairs to match against the entities.

    Returns:
        dict: A dictionary of the selected entities, where the key is the entity ID and the value is the entity object.
    """
    with SQLiteConnection() as cur:
        # Build the SQL query dynamically
        query = f"SELECT * FROM {cls.__name__.lower()} WHERE "
        query += " AND ".join(f"{key} = ?" for key in attrs.keys())

        # Execute the query and fetch the results
        data = cur.execute(query, list(attrs.values()))
        results = data.fetchall()

        # Map the results to objects and return as a dictionary
        objects = dict()
        for row in results:
            entity = cls(*row[1:])
            objects[row[0]] = entity

        return objects
