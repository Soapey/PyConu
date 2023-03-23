from dataclasses import dataclass


@dataclass
class Item:
    id: int
    name: str
    comments: str

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
