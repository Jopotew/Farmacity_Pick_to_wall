from dataclasses import dataclass
from gpiozero import Button


@dataclass
class ButtonPositionModel:
    """
    Represents a button associated with a specific position on a grid.

    Attributes:
        grid_pos (int): The position on the grid.
        button (Button): A GPIO button instance representing the physical button.
    """

    grid_pos: int
    button: Button

    @staticmethod
    def fromDict(grid_pos: int, button: Button):
        """
        Creates a ButtonPositionModel instance from a dictionary-like input.

        Args:
            grid_pos (int): The grid position.
            button (Button): The GPIO button instance.

        Returns:
            ButtonPositionModel: An instance of the ButtonPositionModel.
        """
        return ButtonPositionModel(grid_pos, button)

    def input(self):
        """
        Waits for the button to be pressed. This method blocks until the button press is detected.
        """
        self.button.wait_for_press()
