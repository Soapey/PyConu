from conu.db.SQLiteConnection import SQLiteConnection


class Site:
    def __init__(
        self, id: int = None, name: str = None, address: str = None, suburb: str = None
    ) -> None:
        self.id = id
        self.name = name
        self.address = address
        self.suburb = suburb

    @classmethod
    def get_listingview_table_data(cls, main_window) -> list[tuple]:

        current_user = main_window.current_user

        if not current_user:
            return

        with SQLiteConnection() as cur:
            rows = cur.execute(
                """
                SELECT site.id, site.name, site.address, site.suburb
                FROM site;
                """
            ).fetchall()

        return rows
