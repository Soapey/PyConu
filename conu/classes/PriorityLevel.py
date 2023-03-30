from conu.db.QueryExporter import QueryExporter
from conu.db.SQLiteConnection import SQLiteConnection
from conu.helpers import select_directory


class PriorityLevel:
    def __init__(
        self, id: int = None, name: str = None, days_until_overdue: int = None
    ) -> None:
        self.id = id
        self.name = name
        self.days_until_overdue = days_until_overdue

    @classmethod
    def get_listingview_table_data(cls, main_window, export_to_excel = False) -> list[tuple]:

        current_user = main_window.current_user

        if not current_user:
            return

        query = """
                SELECT DISTINCT 
                    prioritylevel.id AS 'ID', 
                    prioritylevel.name AS 'Name', 
                    prioritylevel.days_until_overdue AS 'Days Until Overdue'
                FROM prioritylevel;
                """

        params = tuple()

        with SQLiteConnection() as cur:
            rows = cur.execute(query, params).fetchall()

        if export_to_excel:

            directory_path: str = None
            try:
                directory_path = select_directory()
            except:
                pass
            
            if directory_path:
                exporter = QueryExporter(query, params, directory_path, "prioritylevels")
                exporter.to_xlsx()

        return rows
