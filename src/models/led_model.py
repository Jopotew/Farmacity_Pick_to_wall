from dataclasses import dataclass
from gpiozero import LED


@dataclass
class LedModel:
    led_color: str
    raspi_pos: int
