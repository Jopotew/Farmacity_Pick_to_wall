from controller.main_menu_control import menu_controller as menu_controller
from services.wave_service import service as wave_service
from controller.raspi_controller import RaspiController
from ui.menu_ui import MenuUi
from ui.console_ui import Console

"""
This script handles the main flow of a program for order management, integrating user input 
via the console and menu interfaces, managing LED and button configurations, and interfacing 
with Raspberry Pi hardware for GPIO control.
"""


def main():
    """
    Main function that manages the execution of the program, handling user input and controlling
    the flow between different modes (manual setup or barcode scanning). It interacts with various
    services, controllers, and user interfaces to complete the necessary actions.

    The flow is as follows:
    1. Menu UI and Console UI are initialized.
    2. The order service is configured.
    3. The user is presented with a menu of options.
    4. If the user chooses the manual setup option (Option 1), the program allows for searching
       orders by name, ID, or barcode, and printing orders. This continues until the wave is completed.
    5. If the user selects the barcode scanning option (Option 2), the program continuously searches
       for barcodes until the wave is completed.
    6. Finally, the program clears any Raspberry Pi GPIO states before exiting.

    Note:
        The `RaspiController` instance is used to ensure that all GPIO states are cleared after execution.
    """
    menu_ui = MenuUi()
    console_ui = Console()
    wave_service.configure()

    try:
        option = console_ui.menu()
        if option == 1:
            print("Manual setup")
            while True:
                if wave_service.check_wave_completion():
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
                if wave_service.check_wave_completion():
                    break
                menu_controller.search_barcode()

    finally:
        raspi_controller = RaspiController()
        raspi_controller.clear_gpios()


if __name__ == "__main__":
    main()
