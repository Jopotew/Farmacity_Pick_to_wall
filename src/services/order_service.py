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

    def get_orders(self) -> SortedOrder:
        db_service = DatabaseService()

        grid_config_dict = db_service.getGrid()
        grid_config = GridConfig.fromDict(grid_config_dict)
        positions = self.create_positions(grid_config)
        order_dict = db_service.getOrders(positions[-1].position)

        sorted_order = []
        for order, position in zip(order_dict, positions):
            items = []
            for item in order_dict[order]:
                items.append(Item.fromDict(item))
            sorted_order.append(Order(position, items))
        print(sorted_order)
        return sorted_order

    def search_position_of_order(self, sorted_orders, item_A: Item):
        print(item_A)
        for order in sorted_orders:
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
        self, sorted_order: list[Order], search_name: str = None
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
                    print(
                        f"Removed item '{item.item_name}' from order at position {order.position}."
                    )
                    return sorted_order
                
                if order is None:
                    rasp_controller = RaspiController()
                    rasp_controller.turn_completionled_on
                    return sorted_order
                
            print("Item not found in any order.")
        else:
            print("No valid item provided for removal. Orders remain unchanged.")
        return sorted_order  # Always return the original list

    def print_orders(self, orders: SortedOrder):
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
                print(f"    {item.item_name}")

    def search_item(self, item, sorted_order):
        rasp_controller = RaspiController()
        button_service = ButtonDataService()
        pos_order = self.search_position_of_order(sorted_order, item)
        rasp_controller.turn_searchled_on(pos_order)
        button = button_service.define_button(pos_order)
        button.wait_for_press()
        rasp_controller.button_pressed()
        sorted_order = self.remove_from_order(sorted_order, item)
        return sorted_order