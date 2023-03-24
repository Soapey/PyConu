from conu.db.SQLiteConnection import SQLiteConnection


class Assignee:
    def __init__(
        self, id: int = None, name: str = None, description: str = None
    ) -> None:
        self.id = id
        self.name = name
        self.description = description

    @classmethod
    def convert_rows_to_instances(cls, rows) -> dict:

        return {
            row[0]: cls(
                row[0],
                row[1],
                row[2],
            )
            for row in rows
        }

    @classmethod
    def get(cls) -> dict:

        with SQLiteConnection() as cur:

            rows = cur.execute(
                """
                SELECT *
                FROM assignee
                """
            ).fetchall()

        return cls.convert_rows_to_instances(rows)

    @classmethod
    def get_listingview_table_data(cls, main_window) -> list[tuple]:

        current_user = main_window.current_user

        if not current_user:
            return

        with SQLiteConnection() as cur:
            rows = cur.execute(
                """
                SELECT DISTINCT assignee.id, assignee.name, assignee.description
                FROM assignee
                JOIN assigneedepartment ON assignee.id = assigneedepartment.assignee_id
                JOIN userdepartment ON assigneedepartment.department_id = userdepartment.department_id
                WHERE userdepartment.user_id = ?;
                """,
                (current_user.id,),
            ).fetchall()

        return rows
