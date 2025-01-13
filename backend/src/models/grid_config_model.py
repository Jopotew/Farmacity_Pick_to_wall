from dataclasses import dataclass
from typing import Optional


@dataclass
class GridConfig:
    """
    Represents the configuration of a grid for a system.

    Attributes:
        rows (int): The number of rows in the grid.
        columns (int): The number of columns in the grid.
        unavailable_positions (Optional[list[int]]): A list of grid positions that are unavailable.
    """

    rows: int
    columns: int
    unavailable_positions: Optional[list[int]] = None

    @staticmethod
    def fromDict(diccionario):
        """
        Creates a GridConfig instance from a dictionary.

        Args:
            diccionario (dict): A dictionary containing the grid configuration.
                - "gridrow" (int): The number of rows in the grid.
                - "gridcol" (int): The number of columns in the grid.
                - "unavailable_positions" (Optional[list[int]]): A list of unavailable positions (optional).

        Returns:
            GridConfig: An instance of the GridConfig class initialized with the dictionary data.
        """
        return GridConfig(
            diccionario["gridrow"],
            diccionario["gridcol"],
            diccionario.get("unavailable_positions"),
        )
