import sys
import os

# Agregar el directorio `src` al path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, "..")
sys.path.append(src_path)

from time import sleep
from services.order_service import OrderService
from models.button_position_model import ButtonPositionModel
from models.led_position_model import LedPositionModel
from services.led_data_service import LedDataService


class RaspiController:
    leds: LedPositionModel  # roja verde posicion
    button: ButtonPositionModel

    def turn_seachled_on(self, position ):
        leds = LedDataService
        led_list = leds.get_leds()
        print("ON")
        l = led_list[position].search_led
       # l.on()

    def turn_searchled_off(self, position):
        leds = LedDataService
        led_list: list = leds.get_leds()
        print("Off")
        l = led_list[position].search_led
        #l.off()

    def turn_completionled_on(self, position):
        leds = LedDataService
        led_list = leds.get_leds()
        print("ON")
        l = led_list[position].completion_led
       # l.on()

    def turn_completionled_off(self, position):
        leds = LedDataService
        led_list: list = leds.get_leds()
        print("Off")
        l = led_list[position].completion_led
       # l.off()

    def button_pressed(self, sorted_order, item):
        """
        Called when is_button_pressed() is triggered
        """
        self.turn_searchled_off()
        order_service = OrderService()
        sorted_order = order_service.remove_from_order(sorted_order, item)
        return sorted_order


