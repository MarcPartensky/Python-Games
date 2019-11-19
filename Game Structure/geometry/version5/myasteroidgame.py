from myspaceshipgroup import AsteroidGameGroup, GamePlayer, AsteroidGroup, MissileGroup, ShooterGroup
from myentitygroup import EntityGroup
from myrectangle import Rectangle
from mygame import Level, Game


class AsteroidGame(Game):
    def __init__(self, **kwargs):
        level1 = DestroyAsteroids()
        level2 = DestroySpaceShips()
        super().__init__(level1, level2, **kwargs)


class AsteroidLevel(Level):
    """Base class of all asteroid levels."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group.spawn()
        self.dt = 0.05
        self.rectangle = Rectangle((0, 0), (200, 200))

    def show(self, context):
        super().show(context)
        self.rectangle.show(context)

    def newPlayer(self):
        """For now we are adding the base class of a player, but this is a naive approach."""
        g = GamePlayer.random()
        self.group.newPlayer(g)
        return g

    def updateWon(self):
        """Must be overloaded in order to change the won state of the level."""
        pass

    def showWin(self, context):
        """Called when the game is won."""
        context.console("Congratulations! You have won the game!")


class DestroyAsteroids(AsteroidLevel):
    """Level in which the players must destroy all the asteroids to win."""

    def __init__(self, n=10, **kwargs):
        spaceships = ShooterGroup(active=False)
        missiles = MissileGroup()
        asteroids = AsteroidGroup.random(n=n, sparse=100)
        group = AsteroidGameGroup(spaceships, missiles, asteroids)
        super().__init__(group, **kwargs)
        self.asteroids_left = 0

    def show(self, context):
        super().show(context)
        if self.asteroids_left != len(self.group.asteroids):
            self.asteroids_left = len(self.group.asteroids)
            context.console("{} asteroids left".format(self.asteroids_left))

    def updateWon(self):
        self.won = len(self.group.asteroids) == 0


class DestroySpaceShips(AsteroidLevel):
    """Level in which the players must kill themselves to win."""

    def __init__(self, n=10, **kwargs):
        spaceships = ShooterGroup.random(n=n)
        missiles = MissileGroup()
        asteroids = AsteroidGroup()
        group = AsteroidGameGroup(spaceships, missiles, asteroids)
        super().__init__(group, **kwargs)
        self.spaceships_left = 0

    def show(self, context):
        super().show(context)
        if self.spaceships_left != len(self.group.spaceships):
            self.spaceships_left = len(self.group.spaceships)
            context.console("{} spaceships left".format(self.spaceships_left-1))

    def updateWon(self):
        self.won = len(self.group.asteroids) == 0


if __name__ == "__main__":
    from mymanager import GameManager
    game = AsteroidGame()
    m = GameManager(game, controller=[0, 0])
    m()
