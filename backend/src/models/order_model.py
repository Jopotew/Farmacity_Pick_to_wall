from dataclasses import dataclass
from models.position_model import Position
from models.item_model import Item


class Order:
    def __init__(self, items: list[Item]):
        self.items = items
        self.position = None

    def is_empty(self) -> bool:
        """
        Returns True if the order has no items, False otherwise.
        """
        return not self.items

    def remove_items(self, item: Item):
        """
        Removes the specified item from the order.

        Args:
            item (Item): The item to remove.
        """
        self.items.remove(item)

    def set_position(self, position: Position):
        self.position = position
