import os
import pickle
from typing import Any, Dict, Optional
from pyhitt.classes.Base import Base
from pyhitt.helpers import read_config_file


def get(cls: type, id: Optional[int] = None) -> Dict[int, object]:
    """
    Retrieve objects from a pickle file.

    Parameters:
        cls (type): The class to which the retrieved objects belong.
        id (Optional[int]): The ID of the object to retrieve. Defaults to None.

    Returns:
        A dictionary containing the retrieved objects, with the object ID as the key and the object itself as the value.
        If `id` is not None, the dictionary will contain a single key-value pair.

    Raises:
        FileNotFoundError: If the pickle file for the specified class does not exist.
    """
    config = read_config_file()
    database_directory = config['PickleSettings']['database_directory']
    table_name = cls.__name__.lower()

    # Create full file path for the specified table
    file_path = os.path.join(database_directory, f"{table_name}.pickle")

    try:
        with open(file_path, 'rb') as f:
            data = pickle.load(f)
            if id:
                e = data.get(id)
                return e
            else:
                return {e.id: e for e in data.values()}
    except FileNotFoundError:
        raise FileNotFoundError(f"No pickle file found for class {cls.__name__}")


def save(objects: list[Any]) -> None:
    """
    Save a Python object to a pickle file database.

    If the object has an ID, update the corresponding record in the table in the
    database. If the object does not have an ID, assign a new ID and add it as
    a new record to the table in the database.

    Args:
        obj (Any): The Python object to save to the database.
        table_name (str): The name of the table to save the object to.

    Raises:
        ValueError: If the object ID is not found in the table.

    Returns:
        None
    """

    if not objects:
        return

    # Load configuration from file
    config: Dict = read_config_file()

    # Get database directory from configuration
    database_directory: str = config['PickleSettings']['database_directory']
    table_name = objects[0].__class__.__name__.lower()

    # Construct file path based on table name
    file_path: str = os.path.join(database_directory, f"{table_name}.pickle")
    
    # Load existing data from pickle file, if it exists
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            data = pickle.load(f)
    else:
        data = dict()

    # Determine the object ID and update the corresponding record in the table
    max_id = max(data.keys(), default=0)
    objects_added = 0
    obj: Base
    for obj in objects:
        obj_id = obj.id
        if obj_id:
            if obj_id not in data:
                raise ValueError(f"No record with ID {obj_id} exists in table {table_name}")
            data[obj_id] = obj
        # Assign a new ID and add the object as a new record to the table
        else:
            objects_added += 1
            new_id = max_id + objects_added
            obj.id = new_id
            data[new_id] = obj

        # Save updated data to pickle file
        with open(file_path, 'wb') as f:
            pickle.dump(data, f)


def delete(cls: type, id: int) -> None:
    """
    Delete a record from a table in a pickle file database.

    Parameters:
        id (int): The ID of the record to delete.
        table_name (str): The name of the table to delete the record from.

    Raises:
        ValueError: If no record with the given ID exists in the table.

    """
    # Load configuration from file
    config: Dict = read_config_file()

    # Get database directory from configuration
    database_directory: str = config['PickleSettings']['database_directory']
    table_name = cls.__name__.lower()

    # Construct file path based on table name
    file_path: str = os.path.join(database_directory, f"{table_name}.pickle")
    
    # Load existing data from pickle file, if it exists
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            data: Dict = pickle.load(f)
    else:
        data = dict()

    # Check if the record with the given ID exists in the table
    if id not in data:
        raise ValueError(f"No record with ID {id} exists in table {table_name}")
    
    # Remove the record from the table
    del data[id]

    # Save updated data to pickle file
    with open(file_path, 'wb') as f:
        pickle.dump(data, f)