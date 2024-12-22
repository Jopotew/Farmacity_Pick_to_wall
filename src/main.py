from services.bcode_scanner_service import ScannerService
from services.order_service import OrderService
from ui.menu_ui import MenuUi

"""
cambiar leds y buttons en leds y buttons

"""


def main():
    """
    Main program loop to interact with the orders.
    """
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

    # TODO: Agregar que se apaguen los leds de la raspi.
    finally:
        pass
        # print("Cleaning up GPIO...")
        # for position in led_pos:
        #     led_pos[position]["red"].off()
        #     led_pos[position]["green"].off()


if __name__ == "__main__":
    main()
