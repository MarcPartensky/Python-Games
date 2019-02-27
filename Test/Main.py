from mywindow import Window
from mycolors import BLACK,WHITE

from map import Map
from player import Player

import random

class Game:
    def __init__(self):
        self.name="Test"
        self.map_size=[100,20]
        self.map=Map(self.map_size)
        self.window_size=[700,600]
        self.fullscreen=False
        self.window=Window(self.name,self.window_size,self.fullscreen)
        self.player=Player()

    def __call__(self):
        self.show()
        while self.window.open:
            self.window.check()
            self.getInput()
            self.update()
            self.show()

    def getInput(self):
        self.input=self.window.press()

    def update(self):
        self.map.update()
        self.player.update(self.map,self.input)

    def show(self):
        vision=self.player.position+self.player.view
        self.map.show(vision,self.window)


if __name__=="__main__":
    game=Game()
    game()
