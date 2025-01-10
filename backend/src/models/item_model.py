from dataclasses import dataclass


@dataclass
class Item:
    """
    Represents an item in the system.

    Attributes:
        farma_id (str): The Farmacity ID of the item.
        item_name (str): The name of the item.
        bar_code (str): The barcode of the item.
    """

    farma_id: str
    item_name: str
    bar_code: str

    @staticmethod
    def fromDict(dic):
        """
        Creates an Item instance from a dictionary.

        Args:
            dic (dict): A dictionary containing item details with the following keys:
                - "farma_id" (str): The Farmacity ID of the item.
                - "item_name" (str): The name of the item.
                - "bar_code" (str): The barcode of the item.

        Returns:
            Item: An instance of the Item class initialized with the dictionary data.
        """
        return Item(dic["farma_id"], dic["item_name"], dic["bar_code"])
