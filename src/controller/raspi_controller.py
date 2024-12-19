from services.led_data_service import LedDataService
from models.led_position_model import LedPositionModel
from models.button_position_model import ButtonPositionModel

class RaspiController:
    leds : LedPositionModel #roja verde posicion
    button : ButtonPositionModel
    
    def turn_led_on(self, position):
        leds = LedDataService
        led_list: list = leds.get_leds()
        for led in led_list:
            pass

    def turn_led_off(self):
        pass

    def button_pressed(self):
        pass


    