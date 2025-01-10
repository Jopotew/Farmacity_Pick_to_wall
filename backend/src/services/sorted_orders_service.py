from models.position_model import Position
from models.grid_config_model import GridConfig
from models.order_model import Order


class SortedOrder:
    """
    A class representing a sorted order that combines grid configuration and order data.

    This class is used to store and manage information about the grid configuration 
    and an order, along with its associated positions.

    Attributes:
        grid (GridConfig): The grid configuration for the sorted order.
        order (Order): The order details that are part of the sorted order.
        positions (list[Position]): A list of positions associated with the sorted order.

    Methods:
        __init__(self, grid: GridConfig, order: Order):
            Initializes a new SortedOrder instance with the given grid configuration and order.
    """

    positions: list[Position]

    def __init__(self, grid: GridConfig, order: Order):
        """
        Initializes a SortedOrder instance.

        Args:
            grid (GridConfig): The grid configuration object.
            order (Order): The order object containing order details.
        """
        self.grid = grid
        self.order = order
