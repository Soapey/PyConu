from conu.classes.Department import Department
from conu.db.SQLiteConnection import SQLiteConnection


class User:
    def __init__(
        self,
        id: int = None,
        first_name: str = None,
        last_name: str = None,
        job_title: str = None,
        email_address: str = None,
        username: str = None,
        password: str = None,
        permission_level: int = None,
        available: bool = None,
    ) -> None:
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.job_title = job_title
        self.email_address = email_address
        self.username = username
        self.password = password
        self.permission_level = permission_level
        self.available = available

    @classmethod
    def convert_rows_to_instances(cls, rows):

        return {
            row[0]: cls(
                row[0],
                row[1],
                row[2],
                row[3],
                row[4],
                row[5],
                row[6],
                row[7],
                row[8],
            )
            for row in rows
        }

    def get_departments(self) -> dict:

        with SQLiteConnection() as cur:

            rows = cur.execute(
                """
                SELECT DISTINCT * 
                FROM department
                JOIN userdepartment ON department.id = userdepartment.department_id
                WHERE userdepartment.user_id = ?;
                """,
                (self.id,),
            ).fetchall()

        return {row[0]: Department(*row) for row in rows}

    @classmethod
    def get(cls):

        with SQLiteConnection() as cur:
            rows = cur.execute(
                """
                SELECT *
                FROM user;
                """
            ).fetchall()

        return cls.convert_rows_to_instances(rows)

    @classmethod
    def get_listingview_table_data(cls, main_window) -> list[tuple]:

        current_user = main_window.current_user

        if not current_user:
            return

        users = None
        # users = get_by_user_departments(User, current_user.id)

        return [
            (
                user.id,
                user.first_name,
                user.last_name,
                user.job_title,
                user.email_address,
                user.permission_level,
                user.available,
            )
            for user in users
        ]
