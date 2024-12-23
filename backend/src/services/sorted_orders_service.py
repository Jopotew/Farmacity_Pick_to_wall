from models.position_model import Position
from models.grid_config_model import GridConfig
from models.order_model import Order



class SortedOrder:
    positions: list[Position]

    def __init__(self, grid: GridConfig, order: Order):
        self.grid = grid
        self.order = order

    def remove_position(self, position: Position):
        pass