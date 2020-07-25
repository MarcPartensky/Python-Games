#!/usr/bin/env python
from mymanager import Manager
from myrectangle import Rectangle
import mycolors

class BlackJackCarpetDrawer(Manager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.background = Rectangle(-0.5, -0.5, 1, 1, area_color=mycolors.GREEN, fill=True)
        self.rectangles = []

    def show(self):
        self.background.show(self.context)

if __name__ == "__main__":
    b = BlackJackCarpetDrawer()
    b()
