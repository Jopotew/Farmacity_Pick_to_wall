from dataclasses import dataclass
from gpiozero import LED


@dataclass
class LedModel:
    """
    Represents an LED in the system.

    Attributes:
        led_color (str): The color of the LED (e.g., "red", "green").
        raspi_pos (LED): The GPIOZero LED instance representing the physical LED.
    """

    led_color: str
    raspi_pos: LED

    def on(self):
        """
        Turns the LED on by activating the GPIO pin.
        """
        self.raspi_pos.on()

    def off(self):
        """
        Turns the LED off by deactivating the GPIO pin.
        """
        self.raspi_pos.off()
