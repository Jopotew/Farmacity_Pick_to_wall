from gpiozero import LED
from time import sleep

led_pos = {
    1: {"red": LED(2), "green": LED(3)},
    2: {"red": LED(4), "green": LED(17)},
    3: {"red": LED(27), "green": LED(22)},
}
