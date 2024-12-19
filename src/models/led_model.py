from dataclasses import dataclass
from gpiozero import LED


@dataclass
class LedModel:
    led_color: str
    raspi_pos: LED  # led

    def on (self):
        self.raspi_pos.on()
        
    def off(self):
        self.raspi_pos.off()