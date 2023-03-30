from conu.db.QueryExporter import QueryExporter
from conu.db.SQLiteConnection import SQLiteConnection
from conu.helpers import select_directory


class Form:
    def __init__(self, id: int = None, name: str = None, path: str = None) -> None:
        self.id = id
        self.name = name
        self.path = path

    @classmethod
    def get_listingview_table_data(cls, main_window, export_to_excel = False) -> list[tuple]:

        current_user = main_window.current_user

        if not current_user:
            return

        query = """
                SELECT DISTINCT 
                    form.id AS 'ID', 
                    form.name AS 'Name', 
                    form.path AS 'Path'
                FROM form;
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
                exporter = QueryExporter(query, params, directory_path, "forms")
                exporter.to_xlsx()

        return rows
