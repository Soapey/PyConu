import os
import hashlib
import configparser
from typing import Dict, List, Optional, Tuple, Type, Any
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from pyhitt.db.SQLConnection import SQLConnection


def read_config_file(file_path: str = None) -> configparser.ConfigParser:
    """
    Read a config file in the INI format and return the configuration values as a dictionary.

    Args:
        file_path (str, optional): The path to the config file. If None, uses the default CONFIG_PATH.

    Returns:
        dict: A dictionary containing the configuration values.
    """
    CONFIG_PATH: str = "pyhitt/config.ini"

    # If file_path is None, use the default config path
    if file_path is None:
        file_path = CONFIG_PATH

    # Create a ConfigParser object and read the config file
    config: configparser.ConfigParser = configparser.ConfigParser()
    config.read(file_path)

    # Return the config dictionary
    return config


def join_to_project_folder(relative_path: str) -> str:
    """
    Join a relative path to the current project folder path and return the full path.

    Args:
        relative_path: A string that represents the relative path to join.

    Returns:
        A string that represents the full path.
    """
    # Get the absolute path of the current working directory
    cwd: str = os.path.abspath(".")

    # Use os.path.join to join the current working directory with the relative path
    full_path: str = os.path.join(cwd, relative_path)

    # Return the full path
    return full_path


def hash_sha512(input_string: str) -> str:
    """
    Hash a string using the SHA2 512 algorithm and return the hashed value as a hexadecimal string.

    Args:
        input_string (str): The input string to be hashed.

    Returns:
        str: The hashed value as a hexadecimal string.
    """
    try:
        # Convert the input string to a bytes object using UTF-8 encoding
        encoded_string: bytes = input_string.encode("utf-8")

        # Create a new SHA2 512 hash object
        sha512_hash: hashlib._hashlib.HASH = hashlib.sha512()

        # Update the hash object with the encoded input string
        sha512_hash.update(encoded_string)

        # Get the hashed value as a bytes object
        hashed_bytes: bytes = sha512_hash.digest()

        # Convert the hashed value to a hexadecimal string and return it
        hashed_string: str = hashed_bytes.hex()
        return hashed_string
    except Exception as e:
        # Handle any exceptions and return None
        print(f"An error occurred while hashing the input string: {str(e)}")
        return None


def search_entities(
    entities: dict, search_columns: List[str], search_text: str = None
) -> dict:
    """
    Search for objects in a dictionary of entities that have at least one attribute in the search columns list that contains
    the search text.

    Args:
        entities (dict): A dictionary of objects to be searched, where the key value is the id attribute of the object.
        search_columns (List[str]): A list of attribute names on the objects to be searched.
        search_text (str, optional): The text to be searched for in the object attributes. Defaults to None.

    Returns:
        dict: A dictionary of objects that contain the search text in one of their attributes, where the key is the id attribute of the object.

    Raises:
        TypeError: If the search_columns argument is not a list.
        TypeError: If the entities argument is not a dictionary.
    """
    # Check for errors in the arguments
    if not isinstance(entities, dict):
        raise TypeError("entities argument must be a dictionary")
    if not isinstance(search_columns, list):
        raise TypeError("search_columns argument must be a list")

    # If the search text is None or empty, return all entities
    if not search_text:
        return entities

    # Create an empty dictionary to store the matching entities
    matching_entities = dict()

    # Loop through each entity in the entities dictionary
    for entity_id, entity in entities.items():
        # Loop through each attribute in the entity
        for attribute_name in dir(entity):
            # Check if the attribute name is in the search columns list
            if attribute_name in search_columns:
                attribute_value = getattr(entity, attribute_name)
                # Check if the attribute value is a string, if not convert it to one before the comparison
                if not isinstance(attribute_value, str):
                    attribute_value = str(attribute_value)
                # Check if the search text is in the attribute value
                if search_text.lower() in attribute_value.lower():
                    # Add the entity to the matching entities dictionary
                    matching_entities[entity_id] = entity
                    break

    return matching_entities


def convert_sql_to_dict(
    data: List[Tuple], attribute_order: List[str], class_name: Type
) -> Dict[Any, Any]:
    """
    Converts a list of tuples to a dictionary of objects of the specified class, using the provided attribute order.

    Args:
        data: A list of tuples containing the attribute values for each object.
        attribute_order: A list of strings specifying the order of attributes for each object.
        class_name: The class to use for creating objects. The class should be callable with a dictionary of attributes.

    Returns:
        A dictionary with the `id` attribute of each object as the key and the object as the value.

    Raises:
        TypeError: If `class_name` is not callable with a dictionary of attributes.
    """
    try:
        instances = [class_name(**dict(zip(attribute_order, t))) for t in data]
    except TypeError:
        raise TypeError(
            "The specified class is not callable with a dictionary of attributes."
        )

    result_dict = {getattr(instance, "id", None): instance for instance in instances}
    return result_dict


def write_to_table(
    table: QTableWidget,
    entities: Dict[int, object],
    attribute_names: List[str],
    header_names: List[str],
) -> None:
    """
    Populates a QTableWidget with data from a list of entities.

    Args:
        table: A QTableWidget instance to populate with data.
        entities: A dictionary of entities to populate the table with. Each key is an entity id (an integer), and each value is an
            object that has attributes corresponding to the values in the `attribute_names` list.
        attribute_names: A list of attribute names to populate the columns of the table with. The order of the attribute names
            in this list determines the order of the columns in the table.
        header_names: A list of header names to set for the columns of the table. The order of the header names in this list
            must correspond to the order of the attribute names in the `attribute_names` list.

    Raises:
        ValueError: If an AttributeError or TypeError occurs while populating the table.

    Returns:
        None. Populates the table with data and returns None.
    """
    try:
        # Clear the table and set the number of rows to zero
        table.clearContents()
        table.setRowCount(0)

        # Set the horizontal header labels
        table.setHorizontalHeaderLabels(header_names)

        # Create a list of QTableWidgetItem instances to populate the table
        items = [
            QTableWidgetItem(str(getattr(entity, attribute_name)))
            for entity in entities.values()
            for attribute_name in attribute_names
        ]

        # Set the number of rows in the table
        table.setRowCount(len(entities))

        # Populate the table with the items
        for i, item in enumerate(items):
            row = i // len(attribute_names)
            col = i % len(attribute_names)
            table.setItem(row, col, item)

    except (AttributeError, TypeError) as e:
        # If an error occurs while populating the table, raise a ValueError with a detailed error message
        raise ValueError(f"Error occurred while writing data to table: {e}")


def get(
    column_names: List[str], table_name: str, ids: Optional[List[int]] = None
) -> List[Tuple]:
    """
    Retrieves data from a SQL Server table.

    Args:
        column_names: A list of column names to return.
        table_name: The name of the table to retrieve data from.
        ids: A list of integers to filter records by. Defaults to None.

    Returns:
        The result of the `fetchall()` method on the cursor, which is a list of tuples.

    Raises:
        ValueError: If `column_names` or `table_name` is an empty string or None.

    """
    if not column_names or not table_name:
        raise ValueError(
            "Both column_names and table_name must be provided and non-empty."
        )

    # Construct the SQL query
    query_params = list()
    query = "SELECT {} FROM {}".format(", ".join(column_names), table_name)

    if ids:
        query += " WHERE id IN ({})".format(", ".join("?" for _ in ids))
        query_params.extend(ids)

    # Execute the query with the parameters
    with SQLConnection() as cursor:
        cursor.execute(query, query_params)
        return cursor.fetchall()


def delete(table_name: str, id: int) -> Optional[int]:
    """
    Deletes a record with a specified id from a table in a SQL database.

    Args:
        table_name (str): The name of the table to delete from.
        id (int): The id of the record to delete.

    Returns:
        Optional[int]: The number of rows affected by the deletion. Returns None if an error occurs.

    Raises:
        Exception: If an error occurs during the deletion process.

    """
    with SQLConnection() as cursor:
        try:
            # Use a parameterized query to avoid SQL injection attacks
            cursor.execute(
                "DELETE FROM ? WHERE id=?",
                (
                    table_name,
                    id,
                ),
            )
            # Get the number of rows affected by the deletion
            rows_affected = cursor.rowcount
            # Commit the deletion
            cursor.commit()
            # Return the number of rows affected
            return rows_affected
        except Exception as error:
            # If an error occurs, log it and rollback the transaction
            print("Error deleting record: {}".format(error))
            cursor.rollback()
            # Return None to indicate that an error occurred
            return None


def save(entity, attribute_names, table_name):
    # Parameter validation
    if not attribute_names:
        raise ValueError("The attribute_names list must not be empty")
    if not table_name:
        raise ValueError("The table_name string must not be empty")

    try:
        with SQLConnection() as cursor:
            if entity.id:
                # Update an existing row in the table
                set_values = ",".join(f"{name}=?" for name in attribute_names)
                query = f"UPDATE {table_name} SET {set_values} WHERE {entity.id}=?"
                cursor.execute(
                    query,
                    *[getattr(entity, name, "") for name in attribute_names]
                    + [entity.id],
                )
            else:
                # Insert a new row in the table
                column_names = ",".join(attribute_names)
                values = ",".join("?" for _ in attribute_names)
                query = f"INSERT INTO {table_name} ({column_names}) VALUES ({values})"
                cursor.execute(
                    query, *[getattr(entity, name, "") for name in attribute_names]
                )

    except Exception as e:
        # Error handling
        print(f"An error occurred: {e}")
        raise
