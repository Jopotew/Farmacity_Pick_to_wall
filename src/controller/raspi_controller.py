from services.order_service import OrderService
from models.button_position_model import ButtonPositionModel
from models.led_position_model import LedPositionModel
from services.led_data_service import LedDataService
import sys
sys.path.append(
    "d:\\Archivos del Programa\\Proyectos\\Farma\\Farmacity_Pick_to_wall\\src"
)


class RaspiController:
    leds: LedPositionModel  # roja verde posicion
    button: ButtonPositionModel

    def turn_led_on(position):
        leds = LedDataService
        led_list: list = leds.get_leds()
        led_list[position].on

    def turn_led_off(position):
        leds = LedDataService
        led_list: list = leds.get_leds()
        led_list[position].off

    def button_pressed(self, sorted_order, item):
        """
        Called when is_button_pressed is called
        """
        self.turn_led_off()
        order_service = OrderService()
        order_service.remove_from_order(sorted_order, item)


d = RaspiController
d.turn_led_on(1)
