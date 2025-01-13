from gpiozero import LED
from time import sleep

# A dictionary to store LED instances mapped to unique position identifiers.
# Each entry contains two LEDs, representing red and green LEDs for each position.

led_pos = {
    1: {"red": LED(2), "green": LED(3)},    
    2: {"red": LED(4), "green": LED(17)},   
    3: {"red": LED(27), "green": LED(22)},  
}
