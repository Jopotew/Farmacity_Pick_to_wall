from services.order_service import service as order_service
from controller.raspi_controller import RaspiController
from ui.menu_ui import MenuUi
from ui.console_ui import Console


class MenuController:

    def search_name():
        name = input("Enter the item name to search: ")
        item = order_service.search_by_name(name)
        order_service.search_item(item)

    def search_id():
        id = str(input("Enter the item's Farmacity Id Code  to search: "))
        item = order_service.search_by_farma_id(id)
        order_service.search_item(item)

    def search_barcode():
        barcode = str(input("Enter the item's barcode to search: "))
        item = order_service.search_by_barcode(barcode)
        order_service.search_item(item)

    def print_orders():
        order_service.print_orders()


menu_controller = MenuController
