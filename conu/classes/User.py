from dataclasses import dataclass
from conu.classes.Department import Department
from conu.db.SQLiteConnection import SQLiteConnection


@dataclass
class User:
    id: int
    first_name: str
    last_name: str
    job_title: str
    email_address: str
    username: str
    password: str
    permission_level: int
    available: bool

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
