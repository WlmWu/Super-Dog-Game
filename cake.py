from item import Item

class Cake(Item):
    def __init__(self, settings, screen, item_type='cake'):
        super().__init__(settings, screen, item_type)