from myspaceship import Shooter, GamePlayer, GameHunter, Asteroid, Hunter, SpiderBase
from mytree import Tree

class SpaceshipTree(Tree):
    pass

class ShooterSpaceshipTree(SpaceshipTree):
    def __init__(self, m, shooting):
        super().__init__(m)
        self.shooting = shooting


class PlayerTree(SpaceshipTree):
    @classmethod
    def random(cls, n=1):
        """Create a group of 1 random player."""
        players = [(f"Player:{i}", GamePlayer.random()) for i in range(n)]
        return cls(players, shooting=True)

    def shoot(self):
        """Return the list of all missiles shooted."""
        shooted = []
        for entity in self:
            if entity.shooting:
                shooted += entity.shoot()
        return shooted

class AsteroidTree():
    pass

class AsteroidGameTree(Tree):
    def update(self):
        pass




if __name__=="__main__":
    p = PlayerTree.random(10)
    print(p["Player:0"])
