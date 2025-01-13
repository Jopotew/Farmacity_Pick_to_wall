import sys
import os

# Add the `src` directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, "..")
sys.path.append(src_path)


from dataclasses import dataclass
from models.led_model import LedModel


@dataclass
class LedPositionModel:
    """
    Represents the LED configuration for a specific grid position.

    Attributes:
        grid_pos (int): The grid position this LED configuration corresponds to.
        search_led (LedModel): The LED used for indicating search operations (e.g., red LED).
        completion_led (LedModel): The LED used for indicating completion operations (e.g., green LED).
    """

    grid_pos: int
    search_led: LedModel  # Red LED
    completion_led: LedModel  # Green LED

    @staticmethod
    def fromDict(grid_pos: int, dic: dict):
        """
        Creates a LedPositionModel instance from a dictionary.

        Args:
            grid_pos (int): The grid position associated with the LEDs.
            dic (dict): A dictionary containing LED data. It should have two key-value pairs where:
                - Key: The color or identifier of the LED (e.g., "red", "green").
                - Value: The corresponding LED object (gpiozero.LED).

        Returns:
            LedPositionModel: An instance of the LedPositionModel class initialized with the provided data.
        """
        leds = tuple(dic.items())
        return LedPositionModel(
            grid_pos,
            LedModel(leds[0][0], leds[0][1]),
            LedModel(leds[1][0], leds[1][1]),
        )
