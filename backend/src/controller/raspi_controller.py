import sys
import os

# Add the `src` directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, "..")
sys.path.append(src_path)

from time import sleep

from models.button_position_model import ButtonPositionModel
from models.led_position_model import LedPositionModel
from services.led_data_service import LedDataService


class RaspiController:
    """
    Controller class for managing Raspberry Pi GPIOs, including LEDs and buttons.
    """

    leds: LedPositionModel  # LED model with red, green, and position LEDs
    button: ButtonPositionModel  # Button model for input detection

    def turn_search_led(self, status: bool, position: int):
        """
        Turns the search LED on or off at a specified position.

        Args:
            status (bool): True to turn the LED on, False to turn it off.
            position (int): The position of the LED to control.
        """
        leds = LedDataService
        led_list = leds.get_leds()

        if status:
            l = led_list[position - 1].search_led
            l.on()
        else:
            l = led_list[position - 1].search_led
            l.off()

    def turn_completion_led(self, status: bool, position: int):
        """
        Turns the completion LED on or off at a specified position.

        Args:
            status (bool): True to turn the LED on, False to turn it off.
            position (int): The position of the LED to control.
        """
        leds = LedDataService
        led_list = leds.get_leds()

        if status:
            l = led_list[position - 1].completion_led
            l.on()
        else:
            l = led_list[position - 1].completion_led
            l.off()

    def button_pressed(self, position: int):
        """
        Handles the event when a button is pressed at a specific position.

        Args:
            position (int): The position of the button that was pressed.
        """
        self.turn_search_led(False, position)

    def clear_gpios(self):
        """
        Resets all GPIOs by turning off all LEDs at all positions.
        """
        leds = LedDataService
        led_list = leds.get_leds()

        for position, led in enumerate(led_list, start=1):
            self.turn_completion_led(False, position)
            self.turn_search_led(False, position)
