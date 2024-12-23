from services.bcode_scanner_service import ScannerService
from services.order_service import OrderService
from controller.raspi_controller import RaspiController
from ui.menu_ui import MenuUi

"""
cambiar leds y buttons en leds y buttons

"""


def main():
    order_service = OrderService()
    menu_ui = MenuUi()

    sorted_orders = order_service.get_orders()

    try:
        while True:
            
            option = menu_ui.menu()
            if option == 1:  # Name
                name = input("Enter the item name to search: ")
                item = order_service.search_by_name(sorted_orders, name)
                sorted_order = order_service.search_item(item, sorted_orders)

            elif option == 2:  # farma_id
                id = int(input("Enter the item's Farmacity Id Code  to search: "))
                item = order_service.search_by_farma_id(sorted_orders, id)
                sorted_order = order_service.search_item(item, sorted_orders)

            elif option == 3:  # barcode
                barcode = int(input("Enter the item's barcode to search: "))
                item = order_service.search_by_barcode(sorted_orders, barcode)
                sorted_order = order_service.search_item(item, sorted_orders)

            elif option == 4:  # camara
                scanner = ScannerService()
                barcode = scanner.scan_and_fetch_product()
                item = order_service.search_by_barcode(sorted_orders, barcode)

                sorted_order = order_service.search_item(item, sorted_orders)

            elif option == 5:
                order_service.print_orders(sorted_orders)

            elif option == 6:  # exit
                break

    finally:
        raspi_controller = RaspiController()
        raspi_controller.clear_gpios()


if __name__ == "__main__":
    main()
