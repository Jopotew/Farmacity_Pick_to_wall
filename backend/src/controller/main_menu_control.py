from services.order_service import service as order_service
from controller.raspi_controller import RaspiController
from ui.menu_ui import MenuUi
from ui.console_ui import Console


class MenuController:
    """
    Controller for managing menu actions and user interactions
    related to item searching and order management.
    """

    @staticmethod
    def search_name():
        """
        Prompts the user to enter an item name to search for.
        Searches for the item by name in the orders and processes it.
        """
        name = input("Enter the item name to search: ")
        item = order_service.search_by_name(name)
        order_service.search_item(item)

    @staticmethod
    def search_id():
        """
        Prompts the user to enter an item's Farmacity ID code to search for.
        Searches for the item by its ID in the orders and processes it.
        """
        id = input("Enter the item's Farmacity ID Code to search: ")
        item = order_service.search_by_farma_id(id)
        order_service.search_item(item)

    @staticmethod
    def search_barcode():
        """
        Prompts the user to enter an item's barcode to search for.
        Searches for the item by its barcode in the orders and processes it.
        """
        barcode = input("Enter the item's barcode to search: ")
        item = order_service.search_by_barcode(barcode)
        order_service.search_item(item)

    @staticmethod
    def print_orders():
        """
        Prints the list of all current orders and their associated items.
        """
        order_service.print_orders()


# Initialize the MenuController instance
menu_controller = MenuController
