from dataclasses import dataclass
from gpiozero import Button

@dataclass
class ButtonPositionModel:
    grid_pos : int
    raspi_pos : Button

    @staticmethod
    def fromDict(grid_pos : int, dic : dict):
        buttons = dic.items()
        return ButtonPositionModel(
            grid_pos, 
            buttons[0],[1]
        )