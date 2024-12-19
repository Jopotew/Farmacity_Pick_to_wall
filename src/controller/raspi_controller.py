from gpiozero import LED, Button
from models.grid_config_model import GridConfig
from models.led_position_model import LedPositionModel
<<<<<<< Updated upstream

class RaspiController:
    conjuntoLEDS : LedPositionModel #roja verde posicion
=======
from services.led_data_service import LedDataService

class RaspiController:
    
    leds : LedDataService #roja verde posicion
>>>>>>> Stashed changes
    Button : Button
    
    
    def __init__(self):
        pass

    def turn_led_on(self):
        pass

    def turn_led_off(self):
        pass

    def button_pressed(self):
        pass


    