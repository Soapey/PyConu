import os
import pickle
from pyhitt.classes.Base import Base
from pyhitt.helpers import read_config_file, instance_matches_expected_values


def get_by_id(cls: type, id: int = None):
    """
    Retrieve objects from a pickle file.

    Parameters:
        cls (type): The class to which the retrieved objects belong.
        id (int, optional): The ID of the object to retrieve. Defaults to None.

    Returns:
        A dictionary containing the retrieved objects, with the object ID as the key and the object itself as the value.
        If `id` is not None, the dictionary will contain a single key-value pair.
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
        return None


def get_by_attribute_value(cls: type, attribute_values: dict) -> dict:
    """Gets all instances of the given class that match the provided attribute values.

    Parameters:
        cls (type): The class to get instances of.
        attribute_values (dict): A dictionary containing attribute names and their
            corresponding expected values.

    Returns:
        A dictionary object that contains all instances of the class that match the
        provided attribute values, with the id of the object as the key.
    """
    # Load the configuration file and extract the database directory path
    try:
        config = read_config_file()
    except FileNotFoundError:
        print("Config file not found.")
        return None

    try:
        database_directory: str = config['PickleSettings']['database_directory']
    except KeyError:
        print("Invalid configuration: 'database_directory' not found.")
        return None

    # Construct the filename for the pickle file
    table_name = cls.__name__.lower()
    file_path = os.path.join(database_directory, f"{table_name}.pickle")

    try:
        # Attempt to open the pickle file for the given class
        with open(file_path, 'rb') as f:
            # Load the data from the file
            data = pickle.load(f)

            # Filter the data to include only instances that match the provided attribute values
            filtered_data = {e.id: e for e in list(filter(lambda i: instance_matches_expected_values(i, attribute_values), data.values()))}

            # Return the filtered data
            return filtered_data

    except FileNotFoundError:
        return None


def save(objects: list) -> None:
    """Save a list of objects to a pickle file.
    
    Parameters:
        objects (list): A list of objects to be saved.
    
    Returns:
        None
    """
    if not objects:
        return None

    try:
        config = read_config_file()
    except FileNotFoundError:
        print("Config file not found.")
        return None

    try:
        database_directory: str = config['PickleSettings']['database_directory']
    except KeyError:
        print("Invalid configuration: 'database_directory' not found.")
        return None

    table_name = objects[0].__class__.__name__.lower()

    file_path: str = os.path.join(database_directory, f"{table_name}.pickle")

    try:
        with open(file_path, 'rb') as f:
            data = pickle.load(f)
    except FileNotFoundError:
        data = dict()

    max_id = max(data.keys(), default=0)
    objects_added = 0
    obj: Base
    for obj in objects:
        obj_id = obj.id
        if obj_id:
            try:
                data[obj_id] = obj
            except KeyError:
                print(f"obj_id: {obj_id} not in data set, cannot update.")
        else:
            objects_added += 1
            new_id = max_id + objects_added
            obj.id = new_id
            data[new_id] = obj

    with open(file_path, 'wb') as f:
        pickle.dump(data, f)


def delete(cls: type, ids: list[int]) -> None:
    """
    Deletes the objects with the specified ids from the pickle file.

    Parameters:
        cls (type): The class of the objects to be deleted.
        ids (list[int]): A list of ids of the objects to be deleted.

    Raises:
        FileNotFoundError: If the pickle file for the specified class does not exist.
    """
    # Read the configuration file to get the database directory path
    config = read_config_file()

    # Get the database directory path and the table name
    try:
        database_directory: str = config['PickleSettings']['database_directory']
    except:
        print("Invalid configuration: 'database_directory' not found.")
        return None
    table_name = cls.__name__.lower()

    # Construct the file path
    file_path: str = os.path.join(database_directory, f"{table_name}.pickle")
    
    # Load the data from the pickle file
    try:
        with open(file_path, 'rb') as f:
            data = pickle.load(f)
    except FileNotFoundError:
        print(f"No pickle file found for class {cls.__name__}")
        return None

    # Delete the objects with the specified ids from the data
    for id in ids:
        if id not in data:
            pass
        del data[id]

    # Write the updated data to the pickle file
    with open(file_path, 'wb') as f: 
        pickle.dump(data, f)
