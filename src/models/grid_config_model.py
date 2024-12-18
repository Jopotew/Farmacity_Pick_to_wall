from dataclasses import dataclass
from typing import Optional


@dataclass
class GridConfig:
    rows: int
    columns: int
    unavailable_positions: Optional[list[int]] = None


    @staticmethod
    def fromDict(diccionario):
        return GridConfig(
            diccionario["rows"],
            diccionario["columns"],
            diccionario.get("unavailable_positions"),
        )


