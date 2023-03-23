from conu.db.SQLiteConnection import SQLiteConnection


class PriorityLevel:
    def __init__(self, id: int, name: str, days_until_overdue: int) -> None:
        self.id = id
        self.name = name
        self.days_until_overdue = days_until_overdue

    @classmethod
    def get_listingview_table_data(cls, main_window) -> list[tuple]:

        current_user = main_window.current_user

        if not current_user:
            return

        with SQLiteConnection() as cur:
            rows = cur.execute(
                """
                SELECT prioritylevel.id, prioritylevel.name, prioritylevel.days_until_overdue
                FROM prioritylevel;
                """
            ).fetchall()

        return rows
