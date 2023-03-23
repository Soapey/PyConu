from conu.classes.Department import Department
from conu.db.SQLiteConnection import SQLiteConnection


class User:
    def __init__(
        self,
        _id: int,
        _first_name: str,
        _last_name: str,
        _job_title: str,
        _email_address: str,
        _username: str,
        _password: str,
        _permission_level: int,
        _available: bool,
    ) -> None:
        self.id = _id
        self.first_name = _first_name
        self.last_name = _last_name
        self.job_title = _job_title
        self.email_address = _email_address
        self.username = _username
        self.password = _password
        self.permission_level = _permission_level
        self.available = _available

    def get_departments(self) -> dict:

        with SQLiteConnection() as cur:

            query = """
            SELECT 
                * 
            FROM 
                department 
            WHERE 
                department.id 
                IN (
                    SELECT 
                        userdepartment.department_id 
                    FROM 
                        userdepartment 
                    WHERE 
                        userdepartment.user_id = ?
                    );
            """

            rows = cur.execute(query, (self.id,)).fetchall()

        departments = dict()
        for row in rows:
            department = Department(*row)
            departments[department.id] = department

        return departments
