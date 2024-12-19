import sys
import os

# Agregar el directorio `src` al path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, '..')
sys.path.append(src_path)

from providers import led_data_provider
from models.led_position_model import LedPositionModel




class LedDataService:
    def get_leds():
        leds = []
        for key, value in led_data_provider.led_pos.items():
            leds.append(LedPositionModel.fromDict(key, value))
        return leds


#led = LedDataService()
#leds = led.get_leds()
#print(leds[0].search_led.raspi_pos)
# # print(leds[Posicion de la grilla].search_led)
