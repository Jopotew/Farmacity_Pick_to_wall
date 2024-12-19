import sys
sys.path.append(
    'd:\\Archivos del Programa\\Proyectos\\Farma\\Farmacity_Pick_to_wall\\src')


from dataclasses import dataclass
from models.led_model import LedModel


@dataclass
class LedPositionModel:
    grid_pos: int
    search_led: LedModel  # rojo
    completion_led: LedModel  # verde
    

    @staticmethod
    def fromDict(grid_pos: int, dic: dict):
        leds = tuple(dic.items())
        return LedPositionModel(
            grid_pos,
            LedModel(leds[0][0], leds[0][1]),
            LedModel(leds[1][0], leds[1][1]),
        )



 