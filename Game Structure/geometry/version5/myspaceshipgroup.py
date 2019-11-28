from myspaceship import Shooter, GamePlayer, GameHunter, Asteroid, Hunter, SpiderBase
from myentitygroup import EntityGroup
from mymanager import EntityManager
from myasteroidofperlin import PerlinAsteroidEntity
from myasteroidofbezier import BezierAsteroid
from myrectangle import Rectangle
from mycollider import Collider

import mycolors


class SpaceShipGroup(EntityGroup):
    """Base class of any spaceship group"""
    def __init__(self, *args, shooting=False, **kwargs):
        self.shooting = shooting
        super().__init__(*args, **kwargs)

    # def shoot(self):
    #     """Direct violation of the principle of substitution of liskov."""
    #     shooted = []
    #     for entity in self:
    #         if isinstance(entity, Shooter):
    #             shooted += entity.shoot()
    #     return shooted


class ActiveSpaceShipGroup(SpaceShipGroup):
    """SpaceShipGroup that deals efficiently with active and inactive spaceships for optimization."""
    @classmethod
    def createFromActives(cls, *spaceships, **kwargs):
        """Suppose all the spaceships actives."""
        return cls.createFromActivesAndPassives(list(spaceships), [], **kwargs)

    @classmethod
    def createFromPassives(cls, *spaceships, **kwargs):
        """Suppose all the spaceships actives."""
        return cls.createFromActivesAndPassives([], list(spaceships), **kwargs)

    @classmethod
    def createFromSpaceShips(cls, *spaceships, **kwargs):
        """Create the advanced group directly from the given spaceships.
        The spaceships are sorted in actives or passives group depending
        on their active state."""
        actives = []
        passives = []
        for spaceship in spaceships:
            if spaceship.active:
                actives.append(spaceship)
            else:
                passives.append(spaceship)
        return cls.createFromActivesAndPassives(actives, passives, **kwargs)

    @classmethod
    def createFromActivesAndPassives(cls, actives=[], passives=[], **kwargs):
        """Create the advanced groups using the list of active and passive spaceships
         and optional spaceship arguments for the advanced group."""
        actives = SpaceShipGroup(*actives)
        passives = SpaceShipGroup(*passives)
        return cls(actives, passives, **kwargs)

    def __init__(self, actives=SpaceShipGroup(), passives=SpaceShipGroup(), **kwargs):
        super().__init__(actives, passives, **kwargs)
        self.activate()

    def activate(self):
        """Active only the actives"""
        self.actives.activate()

    def getActives(self):
        return self[0]

    def setActives(self, actives):
        self[0] = actives

    def delActives(self):
        self[0].clear()

    actives = property(getActives, setActives)

    def getPassives(self):
        return self[1]

    def setPassives(self, passives):
        self[1] = passives

    def delActives(self):
        self[1].clear()

    passives = property(getPassives, setPassives)

    def append(self, spaceship):
        """Add a spaceship to the right category depending if it is passive or not."""
        if spaceship.active:
            self.actives.append(spaceship)
        else:
            self.passives.append(spaceship)

    def shoot(self):
        shooted = []
        for entity in self:
            if entity.shooting:
                shooted.append(entity.shoot())
        return shooted


class PlayerGroup(SpaceShipGroup):
    @classmethod
    def random(cls, n=1, **kwargs):
        """Create a group of 1 random player."""
        players = [GamePlayer.random() for i in range(n)]
        return cls(*players, shooting=True, **kwargs)

    def shoot(self):
        """Return the list of all missiles shooted."""
        shooted = []
        for entity in self:
            if entity.shooting:
                shooted += entity.shoot()
        return shooted


class AsteroidGroup(EntityGroup):
    """Group of asteroids."""
    @classmethod
    def random(cls, n=10, size=10, sparse=10, **kwargs):
        """Create n random asteroids of given size."""
        entities = [Asteroid.random(size=10) for i in range(n)]
        g = cls(*entities, **kwargs)
        g.spread(sparse)
        return g


class ShooterGroup(SpaceShipGroup):
    """Group of shooter."""
    @classmethod
    def random(cls, n=10, **kwargs):
        """Create a group of n random spaceships."""
        entities = [Shooter.random() for i in range(n)]
        return cls(*entities, **kwargs)

    def __init__(self, *args, shooting=True, **kwargs):
        super().__init__(*args, shooting=shooting, **kwargs)

    def shoot(self):
        """Return the list of all missiles shooted."""
        shooted = []
        for entity in self:
            if entity.shooting:
                shooted += entity.shoot()
        return shooted


class HunterGroup(ShooterGroup):
    """Group of hunters."""
    @classmethod
    def random(cls, n=10, **kwargs):
        """Create a group of n random hunters."""
        hunters = [Hunter.random() for i in range(n)]
        return cls(*hunters, **kwargs)

    def retarget(self, target):
        for hunter in self:
            hunter.retarget(target)


class GameSpaceShipGroup(SpaceShipGroup):
    @classmethod
    def random(cls, nh=10, nb=2, **kwargs):
        """Create a random spaceship group."""
        player = GamePlayer.random(side_color=mycolors.BLUE)
        bases = [SpiderBase.random(color=mycolors.RED) for i in range(nb)]
        for base in bases:
            base.spread(10)
        hunters = [GameHunter.random(target=player, side_color=mycolors.YELLOW) for i in range(nh)]
        return cls(player, *bases, *hunters, **kwargs)

    def shoot(self):
        """Kind of careful shoot just to make it work. Non rigorous at all."""
        shooted = []
        for entity in self:
            if entity.shooting:
                shooted += entity.shoot()
        return shooted


class SuperSpaceShipGroup(SpaceShipGroup):
    @classmethod
    def random(cls, **kwargs):
        """Random super spaceship group."""
        player_group = PlayerGroup.random(active=True)
        return cls(player_group, **kwargs)

    def __init__(self, *spaceships, **kwargs):
        """Create a super spaceship group which is a spaceship group of group with a player group."""
        if len(spaceships) == 0:
            spaceships = [PlayerGroup()]
        super().__init__(*spaceships, **kwargs)

    def shoot(self):
        shooted = []
        for group in self:
            if group.shooting:
                shooted.extend(group.shoot())
        return shooted

    def getPlayers(self):
        """Get the player group."""
        return self.entities[0]

    def setPlayers(self, players):
        """Set the player group."""
        self.entities[0] = players

    players = property(getPlayers, setPlayers)

    def clean(self):
        for group in self[1:]:
            group.clean()


class MissileGroup(EntityGroup):
    @classmethod
    def random(cls, n, missile_kwargs={}, **kwargs):
        """Create a missile group of random missiles. This is rarely needed
        since missiles are shooted from spaceships in practice."""
        missiles = [Missile.random(**missile_kwargs) for i in range(n)]
        return cls(*missiles, **kwargs)


class AsteroidGameGroup(EntityGroup):
    """General asteroid game group."""

    def __init__(self,
                 spaceships=None,
                 missiles=None,
                 asteroids=None,
                 collider=Collider(),
                 ):
        """Create an asteroid game group using the groups of spaceships, missiles and asteroids."""
        if spaceships is None:
            spaceships = SuperSpaceShipGroup(active=True)
        if missiles is None:
            missiles = MissileGroup(active=False)
        if asteroids is None:
            asteroids = AsteroidGroup(active=False)
        self.collider = collider
        super().__init__(spaceships, missiles, asteroids)

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
        self.entities[2] = group

    def delAsteroids(self):
        del self.entities[2]

    asteroids = property(getAsteroids, setAsteroids, delAsteroids)

    def update(self, dt):
        """Update the super group."""
        # Update the group
        super().update(dt)
        # Update collisions
        self.updateCollisions()
        # Shoot missiles
        self.missiles.extend(self.spaceships.shoot())
        # Clean the groups
        self.clean()

    def updateCollisions(self):
        """Update the collisions of the group."""
        self.collider.multiChocs(self.missiles, self.spaceships, hitting1=True, killing1=True)
        self.collider.multiChocs(self.missiles, self.asteroids, hitting1=True, killing1=True)
        self.collider.multiChocs(self.spaceships, self.asteroids, killing=True)
        # self.collider.soloChocs(self.asteroids, bouncing=True)

    def clean(self):
        """Clean the asteroids, missiles and spaceships"""
        self.asteroids.clean()
        self.missiles.clean()
        self.spaceships.clean()

    def newPlayer(self, player):
        self.spaceships.players.append(player)

    def reactMouseMotion(self, position):
        self.spaceships.reactMouseMotion(position)

    def reactKeyDown(self, key):
        self.spaceships.reactKeyDown(key)

    def reactMouseButtonDown(self, button, position):
        self.spaceships.reactMouseButtonDown(button, position)

    def getPlayers(self):
        return self.spaceships.players

    def setPlayers(self, players):
        self.spaceships.players = players

    players = property(getPlayers, setPlayers)


class AsteroidGameGroupTest(AsteroidGameGroup):
    @classmethod
    def random(cls, nspaceships=10, nmissiles=0):
        """Create a random game group."""
        spaceships = GameSpaceShipGroup.random(nspaceships, active=True)
        missiles = MissileGroup.random(nmissiles)
        perlin_asteroids = AsteroidGroup.randomOfType(PerlinAsteroidEntity, n=0, size=10)
        bezier_asteroids = AsteroidGroup.randomOfType(BezierAsteroid, n=2, size=10)
        asteroids = perlin_asteroids + bezier_asteroids
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
        """Create n asteroids using the optional size and sparse arguments."""
        g = AsteroidGroup.random(n=n, active=False, size=size, sparse=sparse)
        return g


class AsteroidGameTester(EntityManager):
    """Tester of the asteroid game objects."""
    def __init__(self, **kwargs):
        """Create a spaceship game only using the optional arguments of the
        manager."""
        super().__init__(**kwargs)
        g = AsteroidGameGroupTest()
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
    game = AsteroidGameTester(dt=0.1, friction=0.1, build=True)
    game()
