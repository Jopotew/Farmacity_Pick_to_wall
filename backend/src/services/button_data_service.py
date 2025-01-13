import sys
import os

# Add the `src` directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, "..")
sys.path.append(src_path)

from providers import button_data_provider
from models.button_position_model import ButtonPositionModel


class ButtonDataService:
    """
    A service class responsible for handling button data and interactions.

    This class provides methods to retrieve button data and define a specific button
    based on its position.

    Methods:
        get_button(self):
            Retrieves and returns a list of ButtonPositionModel objects created from
            button data provided by the button_data_provider.

        define_button(self, position):
            Retrieves the ButtonPositionModel object for a specific button based on
            the provided position (1-based index).
    """

    def get_button(self):
        """
        Retrieves button data from the button_data_provider and maps it to
        ButtonPositionModel objects.

        Returns:
            list: A list of ButtonPositionModel objects created from the button data.
        """
        button = []
        for key, value in button_data_provider.button_pos.items():
            button.append(ButtonPositionModel.fromDict(key, value))
        return button

    def define_button(self, position):
        """
        Retrieves the button at a specific position.

        Args:
            position (int): The position of the button (1-based index).

        Returns:
            ButtonPositionModel: The ButtonPositionModel object for the specified position.
        """
        button = self.get_button()[position - 1]
        return button
