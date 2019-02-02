from mypannel import Pannel
from mybutton import Button


class Page:
    def __init__(self,name,pannels,buttons):
        """Create a page object using name, pannels and buttons."""
        self.name=name
        self.pannels=pannels
        self.buttons=buttons
    def load(self):
        pass
