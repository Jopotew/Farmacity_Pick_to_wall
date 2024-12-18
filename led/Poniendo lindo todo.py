from dataclasses import dataclass
from button_led_position import led_pos, button_pos
from typing import Optional
from gpiozero import LED, Button


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


@dataclass
class Item:
    farma_id: str
    item_name: str
    bar_code: str

    @staticmethod
    def fromDict(dic):
        return Item(dic["farma_id"], dic["item_name"], dic["bar_code"])


@dataclass
class Position:
    row: int
    col: int
    position: int


@dataclass
class Order:
    position: Position
    items: list[Item]


@dataclass
class LedModel:
    led_color: str
    raspi_pos: LED


@dataclass
class LedPositionModel:
    grid_pos: int
    completion_led: LedModel  # verde
    search_led: LedModel  # rojo

    @staticmethod
    def from_dict(grid_pos: int, dic: dict):
        leds = dic.items()
        (('green', 1), ('red', 2))
        return LedPositionModel(
            grid_pos,
            LedModel(leds[0][0], leds[0][1]),
            LedModel(leds[1][0], leds[1][1]),
        )


# TODO:
# button


class ButtonPositionModel:
    grid_pos: int
    raspi_pos: int


def proceso():
    led_positions = []
    for key, value in led_pos.items():
        led_positions.append(
            LedPositionModel.from_dict(key, value)
        )

    LedPositionModel.completion_led

# Service ----------------------------------------------------------------


class SortedOrder:
    positions: list[Position]

    def __init__(self, grid: GridConfig, order: Order):
        self.grid = grid
        self.order = order

    def remove_position(self, position: Position):
        pass


class DatabaseService:
    def getGrid(self):
        return data.grid_config

    def getOrders(self):
        return data.order_wave


class OrderService:
    def create_positions(self, grid: GridConfig):
        positions = []
        position = 1
        for row in range(grid.rows):
            for col in range(grid.columns):
                if grid.unavailable_positions is None:
                    positions.append(Position(row, col, position))
                elif position not in grid.unavailable_positions:
                    positions.append(Position(row, col, position))
                position += 1
        return positions

    def getOrders(self) -> SortedOrder:
        grid_config_dict = DatabaseService().getGrid()
        order_dict = DatabaseService().getOrders()

        grid_config = GridConfig.fromDict(grid_config_dict)
        positions = self.create_positions(grid_config)

        sorted_order = []
        for order, position in zip(order_dict, positions):
            items = []
            for item in order_dict[order]:
                items.append(Item.fromDict(item))

            sorted_order.append(Order(position, items))

        return sorted_order

    def search_by_name(self, sorted_order: list[Order], search_name: str = None) -> Item:
        for order in sorted_order:
            for item in order.items:
                if item.item_name.lower().startswith(search_name):
                    return item
        return None

    def search_by_farma_id(self, sorted_order: list[Order], farma_id: int) -> Item:
        for order in sorted_order:
            for item in order.items:
                if item.farma_id == farma_id:
                    return item
        return None

    def search_by_barcode(self, sorted_order: list[Order], barcode_id: int) -> Item:
        for order in sorted_order:
            for item in order.items:
                if item.bar_code == barcode_id:
                    return item
        return None


# Controller LEDs for Raspi ------------------------------------------------


class LedController:
    search_led: LED

    def __init__(self):
        pass

    def turn_on(self):
        pass

    def turn_off(self):
        pass


def main():
    orderService = OrderService()

    imprimir(orderService.getOrders())


def imprimir(orders):
    for order in orders:
        print(order.position)
        for item in order.items:
            print(f'    {item}')


if __name__ == '__main__':
    main()
