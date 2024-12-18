from dataclasses import dataclass
from models.position_model import Position
from models.item_model import Item

@dataclass
class Order:
    position: Position
    items: list[Item]
