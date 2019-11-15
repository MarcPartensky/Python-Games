from myspaceshipgroup import SpaceShipGroup, GamePlayer

class AsteroidDuo:
    def __init__(self):
        player1 = GamePlayer.random()
        player2 = GamePlayer.random()
        self.group = SpaceShipGroup(player1, player2)
        self.dt = 0.1

    def update(self):
        self.group.update(self.dt)












