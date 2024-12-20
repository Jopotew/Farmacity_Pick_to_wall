from dataclasses import dataclass
from gpiozero import Button


@dataclass
class ButtonPositionModel:
    grid_pos: int
    raspi_pos: int  # Button

    @staticmethod
    def fromDict(grid_pos: int, raspi_pos: int):
        return ButtonPositionModel(
            grid_pos,
            raspi_pos
        )
