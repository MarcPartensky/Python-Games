from myspaceship import Shooter, GamePlayer, GameHunter, Asteroid, Hunter, SpiderBase
from mydictmap import Map

class SpaceshipMap(TreeMap):
    pass

class ShooterSpaceshipMap(SpaceshipMap):
    def __init__(self, map, shooting):
        super().__init__(map)
        self.shooting = shooting


class PlayerMap(SpaceshipMap):
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

class AsteroidMap()

class AsteroidGameMap(Map):
    def update(self):




if __name__=="__main__":
    p = PlayerMap.random(10)
    print(p["Player:0"])
