from conu.db.SQLiteConnection import SQLiteConnection


class Form:
    def __init__(self, id: int, name: str, path: str) -> None:
        self.id = id
        self.name = name
        self.path = path

    @classmethod
    def get_listingview_table_data(cls, main_window) -> list[tuple]:

        current_user = main_window.current_user

        if not current_user:
            return

        with SQLiteConnection() as cur:
            rows = cur.execute(
                """
                SELECT form.id, form.name, form.path
                FROM form;
                """
            ).fetchall()

        return rows
