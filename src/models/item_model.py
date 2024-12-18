from dataclasses import dataclass

@dataclass
class Item:
    farma_id: str
    item_name: str
    bar_code: str

    @staticmethod
    def fromDict(dic):
        return Item(dic["farma_id"], dic["item_name"], dic["bar_code"])
