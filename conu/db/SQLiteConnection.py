import os
import sqlite3
from conu.classes.User import User
from conu.classes.Department import Department
from conu.classes.UserDepartment import UserDepartment
from conu.classes.PriorityLevel import PriorityLevel
from conu.helpers import read_config_file, join_to_project_folder, hash_sha512


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
            self.file_path = config["SQLiteSettings"]["database_file"]

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


def init_db(file_path: str = None, clean: bool = False):

    if not file_path:
        # Read the configuration file to get the database directory
        config = read_config_file()
        file_path = config["SQLiteSettings"]["database_file"]

    if clean and os.path.exists(file_path):
        os.remove(file_path)

    script_path = join_to_project_folder(r"conu\db\init.sql")
    with open(script_path, "r") as script:
        script_contents = script.read()
        with SQLiteConnection() as cur:
            cur.executescript(script_contents)


def save_by_list(entities: list) -> list:
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
    return_entities = list()

    with SQLiteConnection() as cur:

        # Get the column names for the entity
        columns = [
            attr
            for attr in dir(entities[0])
            if not callable(getattr(entities[0], attr)) and not attr.startswith("__")
        ]

        # If the entity has an id, update the existing row in the table. Otherwise, insert a new row into the table.
        for entity in entities:

            cls = entity.__class__
            table_name = entity.__class__.__name__.lower()
            values = [getattr(entity, col) for col in columns]

            if entity.id:
                print("Updating entity", entity)
                update_query = f"UPDATE {table_name} SET {', '.join([f'{col} = ?' for col in columns])} WHERE id = ? RETURNING *;"
                updated_entity = cur.execute(
                    update_query, (*values, entity.id)
                ).fetchone()
                return_entities.append(cls(*updated_entity))
            else:
                print("Inserting entity", entity)
                insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['?' for col in columns])}) RETURNING *;"
                inserted_entity = cur.execute(insert_query, values).fetchone()
                return_entities.append(cls(*inserted_entity))

    print("Returning entities:", return_entities)

    return return_entities


def add_test_data(file_path: str = None):

    if not file_path:
        # Read the configuration file to get the database directory
        config = read_config_file()
        file_path = config["SQLiteSettings"]["database_file"]

    users = [
        User(
            id=None, 
            first_name="1", 
            last_name="1", 
            job_title="1", 
            email_address="n/a", 
            username="u1", 
            password=hash_sha512("u1"), 
            permission_level=1, 
            available=1
        ),
        User(
            id=None, 
            first_name="2", 
            last_name="2", 
            job_title="2", 
            email_address="n/a", 
            username="u2", 
            password=hash_sha512("u2"), 
            permission_level=2, 
            available=1
        ),
        User(
            id=None, 
            first_name="3", 
            last_name="3", 
            job_title="3", 
            email_address="n/a", 
            username="u3", 
            password=hash_sha512("u3"), 
            permission_level=3, 
            available=1
        ),
        User(
            id=None, 
            first_name="4", 
            last_name="4", 
            job_title="4", 
            email_address="n/a", 
            username="u4", 
            password=hash_sha512("u4"), 
            permission_level=4, 
            available=1
        ),
    ]

    departments = [
        Department(None, "Maintenance"),
        Department(None, "Environmental"),
        Department(None, "Work, Health & Safety"),
        Department(None, "Transport"),
    ]

    prioritylevels = [
        PriorityLevel(None, "Very High", 3),
        PriorityLevel(None, "High", 7),
        PriorityLevel(None, "Medium", 14),
        PriorityLevel(None, "Low", 31),
        PriorityLevel(None, "Monitoring", 183),
    ]
    

    save_by_list(users)
    save_by_list(departments)
    save_by_list(prioritylevels)

    users = select_by_attrs_dict(User)
    departments = select_by_attrs_dict(Department)

    userdepartments = list()

    for user_id in [id for id in users]:
        for department_id in [id for id in departments]:
            userdepartments.append(UserDepartment(None, user_id, department_id))

    save_by_list(userdepartments)


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
        delete_query = f"DELETE FROM {table_name} WHERE {' AND '.join(f'{attr} = ?' for attr in attrs)} RETURNING *;"
        deleted_entity_tuples = cur.execute(
            delete_query, tuple(attrs.values())
        ).fetchall()
        deleted_entities = [cls(*t) for t in deleted_entity_tuples]
        print("Deleted entities:", deleted_entities)


def select_by_attrs_dict(cls: type, attrs: dict = None) -> dict:
    """
    Selects all entities of the given class that match the specified attribute-value pairs.

    Parameters:
        cls (type): The class of the entities to select.
        attrs (dict): A dictionary of attribute-value pairs to match against the entities.

    Returns:
        dict: A dictionary of the selected entities, where the key is the entity ID and the value is the entity object.
    """
    with SQLiteConnection() as cur:

        if not attrs:
            query = f"SELECT * FROM {cls.__name__.lower()}"
            results = cur.execute(query).fetchall()
        else:
            # Build the SQL query dynamically
            query = f"SELECT * FROM {cls.__name__.lower()} WHERE "
            query += " AND ".join(f"{key} = ?" for key in attrs.keys())

            # Execute the query and fetch the results
            data = cur.execute(query, list(attrs.values()))
            results = data.fetchall()

        # Map the results to objects and return as a dictionary
        objects = dict()
        for row in results:
            entity = cls(*row)
            objects[entity.id] = entity

        return objects


def get_by_user_departments(cls: type, user_id: int):

    fetch_table_name = cls.__name__.lower()
    joint_table_name = f"{cls.__name__}Department"

    with SQLiteConnection() as cur:

        query = """
            SELECT * 
            FROM {} 
            WHERE id IN (
                SELECT {} FROM {} 
                WHERE department_id IN (
                    SELECT department_id FROM userdepartment WHERE user_id = ?
                )
            );""".format(
            fetch_table_name, fetch_table_name + "_id", joint_table_name
        )

        results = cur.execute(query, (user_id,)).fetchall()

        objects = dict()
        for row in results:
            entity = cls(*row)
            objects[entity.id] = entity

        return objects
