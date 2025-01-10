from dataclasses import dataclass
from gpiozero import Button


@dataclass
class ButtonPositionModel:
    grid_pos: int
    button: Button  # Button

    @staticmethod
    def fromDict(grid_pos: int, button: Button):
        return ButtonPositionModel(grid_pos, button)

    def input(self):
        self.button.wait_for_press()
