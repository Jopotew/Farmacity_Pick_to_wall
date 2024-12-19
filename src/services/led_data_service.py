import sys
sys.path.append(
    "d:\\Archivos del Programa\\Proyectos\\Farma\\Farmacity_Pick_to_wall\\src"
    )
from providers import led_data_provider
from models.led_position_model import LedPositionModel




class LedDataService:

    def get_leds():
        leds = []
        for key, value in led_data_provider.led_pos.items():
            leds.append(LedPositionModel.fromDict(key, value))
        return leds


# led = LedDataService()
# leds = led.get_leds()
# print(leds[0].search_led.raspi_pos)
# # print(leds[Posicion de la grilla].search_led)
