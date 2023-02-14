import os
import hashlib
import configparser


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
        encoded_string: bytes = input_string.encode('utf-8')

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