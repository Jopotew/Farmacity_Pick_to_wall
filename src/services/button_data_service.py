

import sys

sys.path.append(
    'c:\\Users\\juanp\\OneDrive\\Desktop\\Github Projects\\Farmacity_Pick_to_wall\\src'
    )

from providers import button_data_provider
from models.button_position_model import ButtonPositionModel


class ButtonDataService:
    def get_button(self):
        button = []
        for key, value in button_data_provider.button_pos.items():
            button.append(ButtonPositionModel.fromDict(key, value))
        return button
    
    def define_button(self, position):
        button = self.get_button()[position]
        return button

    

