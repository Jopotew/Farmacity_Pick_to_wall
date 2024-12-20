from models.grid_config_model import GridConfig
from services.button_data_service import ButtonDataService
from services.order_service import OrderService
from services.database_service import DatabaseService
from providers import led_data_provider
from models.led_position_model import LedPositionModel
from controller.raspi_controller import RaspiController
from ui.menu_ui import MenuUi

"""
cambiar leds y buttons en leds y buttons

"""


def main():
    """
    Main program loop to interact with the orders.
    """
    order_service = OrderService()
    rasp_controller = RaspiController()
    menu_ui = MenuUi()
    button_service = ButtonDataService()

    sorted_orders = order_service.get_orders()

    while True:

        option = menu_ui.menu()
        if option == 1:  # Name
            name = input("Enter the item name to search: ")
            item = order_service.search_by_name(sorted_orders, name)
            pos_order = order_service.search_position_of_order(sorted_orders, item)
            rasp_controller.turn_seachled_on(pos_order)
            button = button_service.define_button(pos_order)
            button.wait_for_press()
            sorted_order = rasp_controller.button_pressed(pos_order, item)

        elif option == 2:  # farma_id
            id = input("Enter the item's Farmacity Id Code  to search: ")
            item = order_service.search_by_farma_id(sorted_orders, id)
            pos_order = order_service.search_position_of_order(sorted_orders, item)
            rasp_controller.turn_seachled_on(pos_order)
            button = button_service.define_button(pos_order)
            button.wait_for_press()
            sorted_order = rasp_controller.button_pressed(pos_order, item)

        elif option == 3:  # barcode
            barcode = input("Enter the item's barcode to search: ")
            item = order_service.search_by_barcode(sorted_orders, barcode)
            pos_order = order_service.search_position_of_order(sorted_orders, item)
            rasp_controller.turn_seachled_on(pos_order)
            button = button_service.define_button(pos_order)
            button.wait_for_press()
            sorted_order = rasp_controller.button_pressed(pos_order, item)

        elif option == 4:
            order_service.print_orders(sorted_order)

        elif option == 5:  # exit
            break


if __name__ == "__main__":
    main()
