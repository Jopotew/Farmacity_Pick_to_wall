import sys
import os

# Agregar el directorio `src` al path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, "..")
sys.path.append(src_path)

from providers import led_data_provider
from models.led_position_model import LedPositionModel


class LedDataService:
    """
    A service class responsible for handling LED data and interactions.

    This class provides methods to retrieve LED data from the LED data provider
    and maps it to appropriate model objects.

    Methods:
        get_leds(self):
            Retrieves and returns a list of LedPositionModel objects created from
            LED data provided by the led_data_provider.
    """

    def get_leds(self):
        """
        Retrieves LED position data from the led_data_provider and maps it to
        LedPositionModel objects.

        Returns:
            list: A list of LedPositionModel objects created from the LED data.
        """
        leds = []
        for key, value in led_data_provider.led_pos.items():
            leds.append(LedPositionModel.fromDict(key, value))
        return leds
