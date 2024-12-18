from dataclasses import dataclass
from led_model import LedModel


@dataclass
class LedPositionModel:
    grid_pos: int
    completion_led: LedModel  # verde
    search_led: LedModel  # rojo

    @staticmethod
    def fromDict(grid_pos: int, dic: dict):
        leds = dic.items()
        return LedPositionModel(
            grid_pos,
            LedModel(leds[0][0], leds[0][1]),
            LedModel(leds[1][0], leds[1][1]),
        )