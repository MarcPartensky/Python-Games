from myspaceshipgroup import AsteroidGameGroup, GamePlayer, \
    AsteroidGroup, MissileGroup, ShooterGroup, HunterGroup, \
    SuperSpaceShipGroup, PlayerGroup
from myrectangle import Rectangle
from mygame import Level, Game

import mycolors
import time

import sys
print(sys.version)


class AsteroidGame(Game):
    def __init__(self, difficulty=10, stage=0, **kwargs):
        """Create an asteroid game using its difficulty, stage and kwargs."""
        levels = [DestroyAsteroids(difficulty),
                  DestroyHunters(difficulty)]
        super().__init__(*levels, stage=stage, **kwargs)


class SoloAsteroidGame(AsteroidGame):
    """Game that can be played solo on a single computer."""
    def __init__(self, difficulty=10, **kwargs):
        self.difficulty = difficulty
        super().__init__(difficulty, **kwargs)


class AsteroidLevel(Level):
    """Base class of all asteroid levels."""
    def __init__(self, group=AsteroidGameGroup(), dt=0.05, **kwargs):
        """Create an asteroid level."""
        self.rectangle = Rectangle(0, 0, 200, 200)
        self.logging_win = False
        self.logging_restart = False
        self.won_time = None
        self.won_duration = 3
        super().__init__(group, dt=dt, **kwargs)

    def start(self):
        pass

    def restart(self):
        self.logging_restart = True
        self.start()

    def show(self, context):
        super().show(context)
        self.group.showBorn(context)
        self.rectangle.show(context)
        if self.logging_win:
            self.showWin(context)
        if self.logging_restart:
            self.showRestart(context)

    def newPlayer(self, **kwargs):
        """For now we are adding the base class of a player, but this is a naive approach."""
        g = GamePlayer.random(**kwargs)
        self.group.newPlayer(g)
        self.group.active = True
        return g

    def showRestart(self, context):
        """Called when the game restarts."""
        context.console("You lost. The level has restarted.", color=mycolors.YELLOW)
        self.logging_restart = False

    def showWin(self, context):
        """Called when the game is won."""
        context.console("Congratulations! You have won the game!", color=mycolors.YELLOW)
        self.logging_win = False

    def update(self):
        """Update the level by updating the groups and checking if the game is won.."""
        super().update()
        self.updateCollisions()
        self.missiles.extend(self.spaceships.shoot())
        self.group.clean()
        self.updateWon()
        self.updateLost()
        self.checkWon()
        self.checkLost()

    def updateWon(self):
        """Update won parameter, this function must be overloaded to make a winnable game."""
        pass

    def updateLost(self):
        """Update lost parameter, the level is lost when all players are dead by default."""
        self.lost = True
        for player in self.players:
            if player.alive:
                self.lost = False
                break

    def checkWon(self):
        """Determine if the level is on or if the victory must be shown when the game is won."""
        if self.won:
            if self.won_time is None:
                self.won_time = time.time()
                self.logging_win = True
            else:
                if time.time() - self.won_time > self.won_duration:
                    self.on = False

    def checkLost(self):
        """Determine if the level is lost or not, if so the game restarts."""
        if self.lost:
            self.restart()
            self.logging_restart = True
            self.lost = False

    def updateCollisions(self):
        """Update the collisions of the group."""
        self.collider.multiChocs(self.missiles, self.spaceships, hitting1=True, killing1=True)
        self.collider.multiChocs(self.missiles, self.asteroids, hitting1=True, killing1=True)
        self.collider.multiChocs(self.spaceships, self.asteroids, killing=True)
        # self.collider.soloChocs(self.asteroids, bouncing=True)

    def getPlayers(self):
        return self.group.players

    def setPlayers(self, players):
        self.group.players = players

    players = property(getPlayers, setPlayers)

    def getSpaceships(self):
        return self.group.spaceships

    def setSpaceships(self, spaceships):
        self.group.spaceships = spaceships

    spaceships = property(getSpaceships, setSpaceships)

    def getAsteroids(self):
        return self.group.asteroids

    def setAsteroids(self, asteroids):
        self.group.asteroids = asteroids

    asteroids = property(getAsteroids, setAsteroids)

    def getMissiles(self):
        return self.group.missiles

    def setMissiles(self, missiles):
        self.group.missiles = missiles

    missiles = property(getMissiles, setMissiles)

    def getCollider(self):
        return self.group.collider

    def setCollider(self, collider):
        self.group.collider = collider

    collider = property(getCollider, setCollider)

class EmptyMultiplayerLevel(AsteroidLevel):
    """Level empty so that players can join to play in multiplayer."""
    def __init__(self, difficulty, **kwargs):
        super().__init__(**kwargs)


class DestroyAsteroids(AsteroidLevel):
    """Level in which the players must destroy all the asteroids to win."""
    def __init__(self, difficulty, **kwargs):
        """Create a level by creating the groups."""
        self.asteroids_left = None
        self.asteroids_total = difficulty
        super().__init__(**kwargs)

    def start(self):
        """Start the game by creating the game group."""
        player = GamePlayer.random()
        players = PlayerGroup(player, activate=True, shooting=True)
        spaceships = SuperSpaceShipGroup(players, active=True)
        asteroids = AsteroidGroup.random(n=self.asteroids_total, sparse=100)
        self.group = AsteroidGameGroup(spaceships, asteroids=asteroids)
        super().start()
        self.asteroids_left = 0

    def show(self, context):
        """Show the level and the number of asteroids left to destroy."""
        if self.asteroids_left != len(self.group.asteroids):
            self.asteroids_left = len(self.group.asteroids)
            context.console("{} asteroids left".format(self.asteroids_left))
        super().show(context)

    def updateWon(self):
        """Determine if the game is won depending on the number of asteroids of the group."""
        self.won = (len(self.group.asteroids) == 0)


class DestroySpaceShips(AsteroidLevel):
    """Level in which the players must kill themselves to win."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.spaceships_left = 0

    def start(self):
        """Start the level."""
        super().start()
        # self.collider.elasticity = 5
        self.spaceships_left = len(self.group.spaceships)

    def updateWon(self):
        """Win when there are no spaceships (that are not players) anymore"""
        self.won = True
        for group in self.group.spaceships[1:]:
            if len(group) > 0:
                self.won = False
                break

    def updateCollisions(self):
        """Update the collisions of the group."""
        self.collider.multiChocs(self.missiles, self.spaceships, hitting1=True, killing1=True)
        self.collider.multiChocs(self.missiles, self.asteroids, hitting1=True, killing1=True)
        self.collider.multiChocs(self.spaceships, self.asteroids, killing=True)
        # self.collider.soloChocs(self.spaceships, bouncing=True)


class DestroyShooters(DestroySpaceShips):
    """Level in which the goal is to destroy all shooters."""
    # For now it is unclear how to use shooters that are not hunters.
    def __init__(self, difficulty, **kwargs):
        """Create the level by creating the groups."""
        self.shooters_total = difficulty
        self.asteroids_total = difficulty
        super().__init__(**kwargs)

    def start(self):
        """Start the game by creating the game group with shooters."""
        player = GamePlayer.random()
        shooters = ShooterGroup.random(n=self.shooters_total)
        players = PlayerGroup(player, shooters, activate=True, shooting=True)
        spaceships = SuperSpaceShipGroup(players, active=True)
        asteroids = AsteroidGroup.random(n=self.asteroids_total, size=10, sparse=100)
        self.group = AsteroidGameGroup(spaceships, asteroids=asteroids)
        super().start()

    def show(self, context):
        """Show the level with the number of spaceships left to destroy."""
        if self.spaceships_left != len(self.group.spaceships[1]):
            self.spaceships_left = len(self.group.spaceships[1])
            context.console("{} shooters left".format(self.spaceships_left))
        super().show(context)


class DestroyHunters(DestroySpaceShips):
    """Level in which the goal is to destroy all hunters."""
    def __init__(self, difficulty, **kwargs):
        """Create the level by creating the groups."""
        self.shooters_total = difficulty
        self.asteroids_total = difficulty
        super().__init__(**kwargs)

    def start(self):
        """Start the game by creating the game group with hunters."""
        player = GamePlayer.random()
        shooters = HunterGroup.random(n=self.shooters_total)
        shooters.spread(100)
        players = PlayerGroup(player, activate=True, shooting=True)
        spaceships = SuperSpaceShipGroup(players, shooters, active=True)
        asteroids = AsteroidGroup.random(n=self.asteroids_total, size=10, sparse=100)
        self.group = AsteroidGameGroup(spaceships, asteroids=asteroids)
        super().start()
        self.group.spaceships[1].retarget(self.players[0])

    def show(self, context):
        """Show the level with the number of spaceships left to destroy."""
        if self.spaceships_left != len(self.group.spaceships[1]):
            self.spaceships_left = len(self.group.spaceships[1])
            context.console("{} hunters left".format(self.spaceships_left))
        super().show(context)


if __name__ == "__main__":
    from mymanager import GameManager
    game = SoloAsteroidGame(stage=1)
    game.start()
    m = GameManager(game, controller=[0, 0, 0])
    m()
