from gpiozero import LED, Button
from models.grid_config_model import GridPosition


class RaspiController:
    search_led: LED
    completion_led : LED
    Button : Button
    grid_position : GridPosition
    
    def __init__(self):
        pass

    def turn_led_on(self):
        pass

    def turn_led_off(self):
        pass

    def button_pressed(self):
        pass


