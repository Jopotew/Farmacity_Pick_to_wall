from dataclasses import dataclass


@dataclass
class Position:
    """
    A class to represent a position in a 2D grid.

    Attributes:
        row (int): The row number of the position.
        col (int): The column number of the position.
        position (int): A unique identifier for the position.

    Methods:
        __init__(self, row: int, col: int, position: int):
            Initializes a new Position instance with the given row, column, and position identifier.
    """

    row: int
    col: int
    position: int
