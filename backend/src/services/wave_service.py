import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, "..")
sys.path.append(src_path)

from models.grid_config_model import GridConfig
from models.position_model import Position
from models.item_model import Item
from services.database_service import DatabaseService
from services.button_data_service import ButtonDataService
from controller.raspi_controller import RaspiController


class WaveService:
    """
    Handles order management and position assignment for a "Pick-to-Wall" system.
    """

    def __init__(self):
        """
        Initializes the order service with an empty list of sorted orders
        and a flag to indicate if the wave of orders is completed.
        """
        self.sorted_orders: list = []
        self.wave_completed: bool = False

    def configure(self):
        """
        Configures the grid positions and orders for the system.

        - Retrieves the grid configuration and the orders from the database.
        - Creates available positions based on the configuration.
        - Assigns orders to the available positions.
        """
        db_service = DatabaseService()
        grid_config = db_service.getGrid()
        positions = self.create_positions(grid_config)
        self.sorted_orders = db_service.getOrders(positions[-1].position)

        for position, order in zip(positions, self.sorted_orders):
            order.set_position(position)

    def create_positions(self, grid: GridConfig) -> Position:
        """
        Creates a list of available positions based on the grid configuration.

        Args:
            grid (GridConfig): The grid configuration containing rows, columns,
                               and unavailable positions.

        Returns:
            list[Position]: A list of available positions.
        """
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
        """
        Searches for an item's position in the orders, activates the corresponding
        LED, and waits for button input to confirm the item has been placed.

        Args:
            item (Item): The item to search for.
        """
        rasp_controller = RaspiController()
        button_service = ButtonDataService()
        pos_order = self.search_position_of_order(item)
        print("Item position:", pos_order)
        rasp_controller.turn_search_led(True, pos_order)
        button = button_service.define_button(pos_order)
        button.input()
        rasp_controller.button_pressed(pos_order)
        self.remove_from_order(item, pos_order)

    def search_position_of_order(self, item_A: Item) -> Position:
        """
        Finds the position of the order containing the specified item.

        Args:
            item_A (Item): The item to search for.

        Returns:
            Position: The position of the order containing the item.
        """
        for order in self.sorted_orders:
            for item_B in order.items:
                if item_B.item_name == item_A.item_name:
                    return order.position.position

    def search_by_name(self, search_name: str = None) -> Item:
        """
        Searches for an item in the sorted orders by its name, starting with the given search term.

        Args:
            search_name (str): The partial or full name of the item to search for.

        Returns:
            Item: The first item that matches the search name, or None if no match is found.
        """
        if not search_name or search_name.strip() == "":
            print("Search name cannot be empty. Please provide a valid name.")
            return None
        else:
            search_name = (
                search_name.lower()
            )  # Normalize input for case-insensitive comparison
            for order in self.sorted_orders:
                for item in order.items:
                    if item.item_name.lower().startswith(search_name):
                        return item

        print(f"No items found matching the name '{search_name}'.")
        return None

    def search_by_farma_id(self, farma_id: str) -> Item:
        """
        Searches for an item by its Farma ID.

        Args:
            farma_id (str): The Farma ID of the item.

        Returns:
            Item: The item matching the Farma ID, or None if not found.
        """
        for order in self.sorted_orders:
            for item in order.items:
                if item.farma_id == farma_id:
                    return item
        return None

    def search_by_barcode(self, barcode_id: str) -> Item:
        """
        Searches for an item by its barcode.

        Args:
            barcode_id (str): The barcode of the item.

        Returns:
            Item: The item matching the barcode, or None if not found.
        """
        for order in self.sorted_orders:
            for item in order.items:
                if item.bar_code == barcode_id:
                    return item
        return None

    def remove_from_order(self, item: Item, pos_order):
        """
        Removes the specified item from the order list and activates
        the completion LED if the order is empty.

        Args:
            item (Item): The item to remove.
            pos_order (Position): The position of the order containing the item.
        """
        if item is not None:
            for order in self.sorted_orders:
                if item in order.items:
                    order.remove_items(item)
                    print(
                        f"Removed item '{item.item_name}' from order at position {pos_order}."
                    )
                self.order_complete(order, pos_order)
        else:
            print("No valid item provided for removal. Orders remain unchanged.")


    def order_complete(self, order, pos_order):
        """
        Marks the order as complete and triggers the completion LED on the Raspberry Pi.

        This method checks if the provided order is empty. If the order is empty,
        it triggers the Raspberry Pi controller to turn on the completion LED 
        at the specified position.

        Args:
            order (Order): The order object that is being checked for completion.
            pos_order (Position): The position of the order containing the item.

        """
        if order.is_empty():
            rasp_controller = RaspiController()
            rasp_controller.turn_completion_led(True, pos_order)
            db_service = DatabaseService()
            db_service.update_order_status(order.order_id, 2)


    def print_orders(self):
        """
        Prints the current state of the orders.
        """
        if not self.sorted_orders:
            print("No orders available.")
            return

        print("Current orders:")
        for order in self.sorted_orders:
            print(f"Position {order.position}:")
            for item in order.items:
                print(f"    {item.item_name}")

    def is_wave_complete(self) -> bool:
        """
        Checks if the wave of orders is complete.

        Returns:
            bool: True if the wave is complete, False otherwise.
        """
        self.check_wave_completion()
        return self.wave_completed

    def check_wave_completion(self) -> bool:
        """
        Updates the wave completion status based on whether all orders are empty.

        Returns:
            bool: True if all orders are empty, False otherwise.
        """
        for order in self.sorted_orders:
            if not order.is_empty():
                self.wave_completed = False
                return
        self.wave_completed = True
        print("Wave completed!")
        return


service = WaveService()
