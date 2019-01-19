from mywindow import *
from mycolors import *

class Entity:
    def __init__(self,position,name="unnamed"):
        self.name=name
        self.position=position
    def move(self):
        pass

class Case:
    def __init__(self):
        pass

class Map:
    def __init__(self,size=[1000,1000]):
        self.size=size
    def generate(self):
        pass

class Player(Entity):
    def __init__(self,name):
        Entity.__init__(name)

    def see(self,game):
        pass


class Game:
    def __init__(self):
        self.start()
        self.loop()
        self.end()

    def start(self):
        self.name="Rpg"
        self.map=Map()
        self.player=Player([0,0],"Marc")
        self.window=Window(self)
        self.map.generate()

    def end(self):
        self.window.kill()

    def show(self):
        self.window.screen.fill(WHITE)
        self.player.see(self)
        self.window.flip()

    def loop(self):
        while self.window.open:
            self.window.check()
            self.show()
            self.player.play(self)

game=Game()
