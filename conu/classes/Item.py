from conu.db.SQLiteConnection import SQLiteConnection


class Item:
    def __init__(self, id: int = None, name: str = None, comments: str = None) -> None:
        self.id = id
        self.name = name
        self.comments = comments

    @classmethod
    def convert_rows_to_instances(cls, rows):

        return {
            row[0]: cls(
                row[0],
                row[1],
                row[2],
            )
            for row in rows
        }

    @classmethod
    def get_listingview_table_data(cls, main_window) -> list[tuple]:

        current_user = main_window.current_user

        if not current_user:
            return

        with SQLiteConnection() as cur:
            rows = cur.execute(
                """
                SELECT DISTINCT item.id, item.name, item.comments
                FROM item
                JOIN itemdepartment ON item.id = itemdepartment.item_id
                JOIN userdepartment ON itemdepartment.department_id = userdepartment.department_id
                WHERE userdepartment.user_id = ?;
                """,
                (current_user.id,),
            ).fetchall()

        return rows
