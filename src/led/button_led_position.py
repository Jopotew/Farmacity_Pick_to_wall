from gpiozero import LED, Button
from time import sleep


led_pos = {1 : {"red": LED(17), "green": LED(22)}, 2 : {"red": LED(11), "green": LED(27)}, 3 : {"red": LED(9), "green": LED(10)} }
button_pos = {1: Button(2), 2: Button(18), 3: Button(15)}



