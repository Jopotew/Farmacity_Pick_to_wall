import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, "..")
sys.path.append(src_path)


from models.grid_config_model import GridConfig
from models.position_model import Position
from models.item_model import Item
from models.order_model import Order
from services.database_service import DatabaseService
from services.sorted_orders_service import SortedOrder
from services.button_data_service import ButtonDataService
from controller.raspi_controller import RaspiController


class OrderService:
    def __init__(self):
        self.sorted_orders = []

    def configure(self):
        db_service = DatabaseService()

        grid_config = db_service.getGrid()
        positions = self.create_positions(grid_config)
        self.sorted_orders = db_service.getOrders(positions[-1].position)

        # Asigno las posiciones disponibles
        for position, order in zip(positions, self.sorted_orders):
            order.set_position(position)

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

    def search_item(self, item):
        rasp_controller = RaspiController()
        button_service = ButtonDataService()
        pos_order = self.search_position_of_order(item)
        rasp_controller.turn_searchled_on(pos_order)
        button = button_service.define_button(pos_order)
        button.wait_for_press()
        rasp_controller.button_pressed(pos_order)
        self.remove_from_order(item)

    def search_position_of_order(self, item_A: Item):
        """
        Returns the position of the order that contains the specified item.

        """
        for order in self.sorted_orders:
            for item_B in order.items:
                if item_B.item_name == item_A.item_name:
                    print(f"IEM FOUND: {item_B.item_name}")
                    pos_order = order.position.position
                    print("POSITION OF THE ORDER: ", pos_order)
                    return pos_order

    # TODO:
    """
    crear condicional que busque articulos con el mismo nombre en distintos pedidos
    ACTRON x 10
    ACTRON x 2O
    tinen el mismo nombre y cuando los buscas saltaria el primero de las listas.
    esto deberia preguntarte cual de los dos estas buscando y que te devuelva ese. 
    """

    def search_by_name(
        self, search_name: str = None
    ) -> Item:
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
            search_name = (
                search_name.lower()
            )  # Normalize input for case-insensitive comparison
            for order in self.sorted_orders:
                for item in order.items:
                    if item.item_name.lower().startswith(search_name):
                        return item

        # If no match is found
        print(f"No items found matching the name '{search_name}'.")
        return None

    def search_by_farma_id(self, farma_id: int) -> Item:
        for order in self.sorted_orders:
            for item in order.items:
                if item.farma_id == farma_id:
                    return item
        return None

    def search_by_barcode(self, barcode_id: int) -> Item:
        for order in self.sorted_orders:
            for item in order.items:
                if item.bar_code == barcode_id:
                    return item
        return None

    def remove_from_order(self, item: Item):
        """
        Removes the specified item from the sorted orders, if found.

        Args:
            sorted_order (list[Order]): The list of orders.
            item (Item): The item to remove.

        Returns:
            list[Order]: The updated list of orders after removing the item.
        """
        if item is not None:
            for order in self.sorted_orders:
                if item in order.items:
                    order.remove_items(item)
                    print(
                        f"Removed item '{item.item_name}' from order at position {order.position}."
                    )

                if order.is_empty():
                    rasp_controller = RaspiController()
                    rasp_controller.turn_completionled_on()

            print("Item not found in any order.")
        else:
            print("No valid item provided for removal. Orders remain unchanged.")

    def print_orders(self):
        """
        Prints the current state of orders.

        Args:
            orders (list[Order]): The list of orders to print.
        """
        if not self.sorted_orders:
            print("No orders available.")
            return

        print("Current orders:")
        for order in self.sorted_orders:
            print(f"Position {order.position}:")
            for item in order.items:
                print(f"    {item.item_name}")


service = OrderService()