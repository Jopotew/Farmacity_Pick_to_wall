from src.services.wave_service import service as wave_service


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
        item = wave_service.search_by_name(name)
        wave_service.search_item(item)

    @staticmethod
    def search_id():
        """
        Prompts the user to enter an item's Farmacity ID code to search for.
        Searches for the item by its ID in the orders and processes it.
        """
        id = input("Enter the item's Farmacity ID Code to search: ")
        item = wave_service.search_by_farma_id(id)
        wave_service.search_item(item)

    @staticmethod
    def search_barcode():
        """
        Prompts the user to enter an item's barcode to search for.
        Searches for the item by its barcode in the orders and processes it.
        """
        barcode = input("Enter the item's barcode to search: ")
        item = wave_service.search_by_barcode(barcode)
        wave_service.search_item(item)

    @staticmethod
    def print_orders():
        """
        Prints the list of all current orders and their associated items.
        """
        wave_service.print_orders()


# Initialize the MenuController instance
menu_controller = MenuController
