import os
import hashlib
import configparser
from typing import List
from conu.ui.PageEnum import Page
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView
import tkinter as tk
from tkinter import filedialog


def navigate(main_window, page: Page):
    main_window.ui.page_handler.setCurrentIndex(page.value)


def read_config_file(file_path: str = None) -> configparser.ConfigParser:
    """
    Read a config file in the INI format and return the configuration values as a dictionary.

    Args:
        file_path (str, optional): The path to the config file. If None, uses the default CONFIG_PATH.

    Returns:
        dict: A dictionary containing the configuration values.
    """
    CONFIG_PATH: str = "conu/config.ini"

    # If file_path is None, use the default config path
    if file_path is None:
        file_path = join_to_project_folder(CONFIG_PATH)

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


def load_entities_into_table(table, entities, attribute_header_dict):
    # Create a QTableWidget with the correct number of rows and columns
    table.clear()
    table.setRowCount(len(entities))
    table.setColumnCount(len(attribute_header_dict.keys()))
    table.setHorizontalHeaderLabels(list(attribute_header_dict.values()))

    header = table.horizontalHeader()

    # Loop through each entity and attribute
    for j, name in enumerate(attribute_header_dict.keys()):

        header.setSectionResizeMode(j, QHeaderView.ResizeToContents)

        for i, entity in enumerate(entities):
            # Check if the attribute exists on the entity
            if hasattr(entity, name):
                # Get the value of the attribute
                value = getattr(entity, name)
                # Set the value in the table widget
                table.setItem(i, j, QTableWidgetItem(str(value)))


def selected_row_id(tbl):

    indexes = tbl.selectedIndexes()

    if len(indexes) == 0:
        return None

    selected_row = indexes[0].row()
    id_column = 0
    id = int(tbl.item(selected_row, id_column).text())

    return id


def select_file_path() -> str:
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    if file_path:
        return file_path
    else:
        return None


def set_button_visibility(buttons: list, is_visible: bool):

    for button in buttons:
        button.setVisible(is_visible)


def clear_widget_children(widget):

    while widget.count():
        child = widget.takeAt(0)
        if child.widget():
            child.widget().deleteLater()
