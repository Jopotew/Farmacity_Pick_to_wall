from dataclasses import dataclass
#from button_led_position import led_pos, button_pos
from typing import Optional
#from gpiozero import LED, Button
import data 



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

"""
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
    def fromDict(grid_pos: int, dic: dict):
        leds = dic.items()
        return LedPositionModel(
            grid_pos,
            LedModel(leds[0][0], leds[0][1]),
            LedModel(leds[1][0], leds[1][1]),
        )
"""

# TODO:
# button

"""
@dataclass
class ButtonPositionModel:
    grid_pos : int
    raspi_pos : Button

    @staticmethod
    def fromDict(grid_pos : int, dic : dict):
        buttons = dic.items()
        return ButtonPositionModel(
            grid_pos, 
            buttons[0],[1]
        )


def proceso():
    led_positions = []
    for key, value in led_pos.items():
        led_positions.append(
            LedPositionModel.from_dict(key, value)
        )

    LedPositionModel.completion_led

"""
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


#TODO:
    """
    crear condicional que busque articulos con el mismo nombre en distintos pedidos
    ACTRON x 10
    ACTRON x 2O
    tinen el mismo nombre y cuando los buscas saltaria el primero de las listas.
    esto deberia preguntarte cual de los dos estas buscando y que te devuelva ese. 
    """
    def search_by_name(self, sorted_order: list[Order], search_name: str = None) -> Item:
        """
        Searches for an item in the sorted orders by its name, starting with the given search term.

        Args:
            sorted_order (list[Order]): The list of orders to search through.
            search_name (str): The partial or full name of the item to search for.

        Returns:
            Item: The first item that matches the search name, or None if no match is found.
        """
        # Check if search_name is None or empty
        if not search_name or search_name.strip() == "":
            print("Search name cannot be empty. Please provide a valid name.")
            return None
        else:
            # Proceed with the search
            search_name = search_name.lower()  # Normalize input for case-insensitive comparison
            for order in sorted_order:
                for item in order.items:
                    if item.item_name.lower().startswith(search_name):
                        return item

        # If no match is found
        print(f"No items found matching the name '{search_name}'.")
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
    
    def remove_from_order(self, sorted_order: list[Order], item: Item) -> list[Order]:
        """
        Removes the specified item from the sorted orders, if found.

        Args:
            sorted_order (list[Order]): The list of orders.
            item (Item): The item to remove.

        Returns:
            list[Order]: The updated list of orders after removing the item.
        """
        if item is not None:
            for order in sorted_order:
                if item in order.items:
                    order.items.remove(item)
                    print(f"Removed item '{item.item_name}' from order at position {order.position}.")
                    return sorted_order
            print("Item not found in any order.")
        else:
            print("No valid item provided for removal. Orders remain unchanged.")
        return sorted_order  # Always return the original list



# Controller LEDs for Raspi ------------------------------------------------

"""
class LedController:
    search_led: LED

    def __init__(self):
        pass

    def turn_on(self):
        pass

    def turn_off(self):
        pass

"""
def main():
    """
    Main program loop to interact with the orders.
    """
    orderService = OrderService()
    sorted_order = orderService.getOrders()

    while True:
        item_name = input("Write the item you are looking for (or type 'exit' to quit): ")
        
        # Handle exit condition
        if item_name.lower() == "exit":
            print("Exiting...")
            break

        # Handle empty input
        if not item_name.strip():
            print("No input given.")
            continue

        # Search for the item
        item = orderService.search_by_name(sorted_order, item_name)
        if item is None:
            print("Item not found or invalid input.")
              
            continue

        # Remove the item if found
        sorted_order = orderService.remove_from_order(sorted_order, item)
        print("Order after removing item:")
        imprimir(sorted_order)




def imprimir(orders):
    """
    Prints the current state of orders.
    
    Args:
        orders (list[Order]): The list of orders to print.
    """
    if not orders:
        print("No orders available.")
        return

    print("Current orders:")
    for order in orders:
        print(f"Position {order.position}:")
        for item in order.items:
            print(f'    {item.item_name}')



if __name__ == '__main__':
    main()
