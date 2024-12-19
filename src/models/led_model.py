from dataclasses import dataclass
from gpiozero import LED


@dataclass
class LedModel:
    led_color: str
<<<<<<< Updated upstream
    raspi_pos: int
=======
    raspi_pos: int #LED
>>>>>>> Stashed changes
