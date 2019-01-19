import Player

class Bot(Player.Player):
    def __init__(self,name=None,skin=None):
        Player.__init__(self)

    def play(self,game):
        if self.alive:
            self.cursor=self.analyze(game.entities)
            self.move()
        else:
            self.spawn(game.map)

    def analyze(self,entities):
        return self.closest(entities).coordonnates
