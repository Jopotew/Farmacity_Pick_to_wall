from controller.main_menu_control import menu_controller as menu_controller
from services.order_service import service as order_service
from controller.raspi_controller import RaspiController
from ui.menu_ui import MenuUi
from ui.console_ui import Console

"""
cambiar leds y buttons en leds y buttons

"""


def main():

    menu_ui = MenuUi()
    console_ui = Console()
    order_service.configure()

    try:
        option = console_ui.menu()
        if option == 1:
            print("Manual setup")
            while True:
                if order_service.check_wave_completion():
                    break
                option = menu_ui.menu()
                if option == 1:
                    menu_controller.search_name()

                elif option == 2:  # farma_id
                    menu_controller.search_id()

                elif option == 3:  # barcode
                    menu_controller.search_barcode()

                elif option == 4:
                    menu_controller.print_orders()

                elif option == 5:  # exit
                    break

        if option == 2:
            while True:

                if order_service.check_wave_completion():
                    break

                menu_controller.search_barcode()

    finally:
        raspi_controller = RaspiController()
        raspi_controller.clear_gpios()


if __name__ == "__main__":
    main()
