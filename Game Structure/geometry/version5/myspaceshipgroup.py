from myspaceship import Shooter, PlayableShooter, TriangleSpaceShip, Asteroid, Hunter, SpiderBase, ShowMotionSpaceShip
from myentitygroup import BasicEntityGroup
from mymanager import EntityManager
from myasteroidofperlin import PerlinAsteroidEntity
from myasteroidofbezier import BezierAsteroid
from myrectangle import Rectangle

import mycolors


class GamePlayer(PlayableShooter, TriangleSpaceShip, ShowMotionSpaceShip):
    pass

class GameHunter(Hunter, TriangleSpaceShip):
    pass

class SpaceShipGroup(BasicEntityGroup):
    pass

class HunterGroup(BasicEntityGroup):
    """Group of hunters."""

    @classmethod
    def random(cls, n=10, **kwargs):
        """Create a group of n random hunters."""
        hunters = [Hunter.random() for i in range(n)]
        return cls(*hunters, **kwargs)


class AsteroidGroup(BasicEntityGroup):
    """Group of asteroids."""

    @classmethod
    def random(cls, n=10, size=10, sparse=10, **kwargs):
        """Create n random asteroids of given size."""
        entities = [Asteroid.random() for i in range(n)]
        g = cls(*entities, **kwargs)
        g.enlarge(size)
        g.spread(sparse)
        return g


class ShooterGroup(SpaceShipGroup):
    """Group of shooter."""

    @classmethod
    def random(cls, n=10, **kwargs):
        """Create a group of n random spaceships."""
        entities = [Shooter.random() for i in range(n)]
        return cls(*entities, **kwargs)

    def getShooted(self):
        """Return the list of all missiles shooted."""
        shooted = []
        for entity in self.entities:
            if entity.shooting:
                shooted.append(entity.shoot())
        return shooted

    def reactMouseMotion(self, position):
        super().reactMouseMotion(position)


class GameSpaceShipGroup(SpaceShipGroup):
    @classmethod
    def random(cls, nh=10, nb=2, **kwargs):
        """Create a random spaceship group."""
        player = GamePlayer.random(side_color=mycolors.BLUE)
        bases = [SpiderBase.random(color=mycolors.RED) for i in range(nb)]
        for base in bases:
            base.spread(10)
        hunters = [GameHunter.random(target=player, side_color=mycolors.YELLOW) for i in range(nh)]
        return cls(player, *bases, *hunters,  **kwargs)

    def getShooted(self):
        """Kind of careful shoot just to make it work. Non rigorous at all."""
        shooted=[]
        for entity in self.entities:
            if isinstance(entity, Shooter):
                if entity.shooting:
                    shooted.append(entity.shoot())
                    entity.shooting=False
        return shooted


class MissileGroup(BasicEntityGroup):
    @classmethod
    def random(cls, n, **kwargs):
        """Create a missile group of random missiles. This is rarely needed
        since missiles are shooted from spaceships in practice."""
        missiles = [Missile.random() for i in range(n)]
        return cls(*missiles, **kwargs)


class GameGroup(BasicEntityGroup):
    def getSpaceShips(self):
        return self.entities[0]

    def setSpaceShips(self, group):
        self.entities[0] = group

    def delSpaceShips(self):
        del self.entities[0]

    spaceships = property(getSpaceShips, setSpaceShips, delSpaceShips)

    def getMissiles(self):
        return self.entities[1]

    def setMissiles(self, group):
        self.entities[1] = group

    def delMissiles(self):
        del self.entities[1]

    missiles = property(getMissiles, setMissiles, delMissiles)

    def getAsteroids(self):
        return self.entities[2]

    def setAsteroids(self, group):
        self.entites[2] = group

    def delAsteroids(self):
        del self.entities[2]

    asteroids = property(getAsteroids, setAsteroids, delAsteroids)

    def update(self, dt):
        """Update the super group."""
        super().update(dt)
        BasicEntityGroup.killOnCollision(self.missiles, self.spaceships)
        BasicEntityGroup.killOnCollision(self.missiles, self.asteroids)
        self.clear()
        self.missiles.extend(self.spaceships.getShooted())

class AsteroidGameGroup(GameGroup):
    @classmethod
    def random(cls, nspaceships=10, nmissiles=0):
        """Create a random game group."""
        spaceships = GameSpaceShipGroup.random(nspaceships, active=True)
        missiles = MissileGroup.random(nmissiles)
        perlin_asteroids = AsteroidGroup.randomOfType(
            PerlinAsteroidEntity, n=0, size=10)
        bezier_asteroids = AsteroidGroup.randomOfType(
            BezierAsteroid, n=2, size=10)
        asteroids = perlin_asteroids + bezier_asteroids
        print(type(asteroids))
        return cls(spaceships, missiles, asteroids)

    def __init__(self, nspaceships=10, nmissiles=0, nasteroids=20):
        """Create a random game group using the optional number of entities of each group.."""
        spaceships = self.createSpaceShips(nspaceships)
        missiles = self.createMissiles(nmissiles)
        asteroids = self.createAsteroids(nasteroids)
        super().__init__(spaceships, missiles, asteroids)

    def createSpaceShips(self, n):
        """Return a group of n random spaceships."""
        return GameSpaceShipGroup.random(n, active=True)

    def createMissiles(self, n):
        """Return a group of n random missiles."""
        return MissileGroup.random(n, active=False)

    def createAsteroids(self, n, size=10, sparse=100):
        """Return a group of n random asteroids."""
        g = AsteroidGroup.random(n=n, active=False, size=size, sparse=sparse)
        # p = PerlinAsteroidEntity.random(active=False)
        # p.enlarge(size)
        # p.spread(sparse)
        # g.append(p)
        return g




class AsteroidGame(EntityManager):
    def __init__(self, **kwargs):
        """Create a spaceship game only using the optional arguments of the
        manager."""
        super().__init__(**kwargs)
        g = AsteroidGameGroup()
        g.spawn()
        # g.activate()
        self.entities = [g]
        self.borns = Rectangle([0, 0], [200, 200])

    def show(self):
        """Show the spaceship game."""
        super().show()
        self.borns.show(self.context)

    def update(self):
        """Update as usual but set the center of the context to the position of
        the entity being played."""
        super().update()
        self.context.position = self.entities[0][0][0].position


if __name__ == "__main__":
    game = AsteroidGame(dt=0.1, friction=0.1, build=True)
    game()
