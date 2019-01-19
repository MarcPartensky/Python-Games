import Player.Player

class Human(Player):
    def __init__(self,name=None,skin=None):
        Player.__init__(self)
    def play(self,game):
        if self.alive:
            game.show(self)
            self.cursor=game.window.point()
            self.move()
        else:
            self.spawn(game.map)
