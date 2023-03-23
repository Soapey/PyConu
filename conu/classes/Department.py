from conu.db.SQLiteConnection import SQLiteConnection


class Department:
    def __init__(self, id: int, name: str) -> None:
        self.id = id
        self.name = name

    @classmethod
    def get_listingview_table_data(cls, main_window) -> list[tuple]:

        current_user = main_window.current_user

        if not current_user:
            return

        with SQLiteConnection() as cur:
            rows = cur.execute(
                """
                SELECT department.id, department.name
                FROM department
                JOIN userdepartment ON department.id = userdepartment.department_id
                WHERE userdepartment.user_id = ?;
                """,
                (current_user.id,),
            ).fetchall()

        return rows
