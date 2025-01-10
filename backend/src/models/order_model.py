from dataclasses import dataclass
from models.position_model import Position
from models.item_model import Item


class Order:
    """
    Represents an order that contains a list of items and an associated position in a grid.

    Attributes:
        items (list[Item]): A list of items in the order.
        position (Position): The grid position assigned to the order.
        order_id (str): A unique identifier for the order.
    """

    def __init__(self, items: list[Item], order_id: str):
        """
        Initializes an Order instance.

        Args:
            items (list[Item]): A list of items in the order.
            order_id (str): A unique identifier for the order.
        """
        self.items: list[Item] = items
        self.position: Position = None
        self.order_id: str = order_id

    def is_empty(self) -> bool:
        """
        Checks if the order is empty (contains no items).

        Returns:
            bool: True if the order has no items, False otherwise.
        """
        return not self.items

    def remove_items(self, item: Item):
        """
        Removes the specified item from the order.

        Args:
            item (Item): The item to remove from the order.
        """
        self.items.remove(item)

    def set_position(self, position: Position):
        """
        Assigns a grid position to the order.

        Args:
            position (Position): The position to assign to the order.
        """
        self.position = position
