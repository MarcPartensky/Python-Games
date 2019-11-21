from myspaceshipgroup import AsteroidGameGroup, GamePlayer, \
    AsteroidGroup, MissileGroup, ShooterGroup, HunterGroup
from myrectangle import Rectangle
from mygame import Level, Game

import mycolors
import time


class AsteroidGame(Game):
    def __init__(self, difficulty=10, stage=0, **kwargs):
        levels = [DestroyAsteroids(difficulty),
                  DestroyShooters(difficulty),
                  DestroyHunters(difficulty)]
        super().__init__(*levels, stage=stage, **kwargs)


class SoloAsteroidGame(AsteroidGame):
    """Game that can be played solo on a single computer."""
    def __init__(self, difficulty=10, **kwargs):
        self.difficulty = difficulty
        super().__init__(difficulty, **kwargs)
        self.player_list = []
        self.makeSoloLevels()

    def makeSoloLevels(self):
        """Make all levels playable solo."""
        for i in range(len(self.levels)):
            self.levels[i].group.active = True
            self.levels[i].group.spaceships.active = True
            player = self.levels[i].newPlayer()
            player.activate()
            self.player_list.append(player)

    def update(self):
        super().update()
        player = self.player_list[self.stage]
        if player is not None:
            if not player.alive:
                self.level.restart(self.difficulty)


class AsteroidLevel(Level):
    """Base class of all asteroid levels."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dt = 0.05
        self.rectangle = Rectangle((0, 0), (200, 200))
        self.logging_win = False
        self.won_time = None
        self.won_duration = 3

    def start(self):
        pass

    def restart(self, *args, **kwargs):
        self.__dict__ = (super().__init__(*args, **kwargs)).__dict__

    def show(self, context):
        super().show(context)
        self.rectangle.show(context)
        if self.logging_win:
            self.showWin(context)

    def newPlayer(self, **kwargs):
        """For now we are adding the base class of a player, but this is a naive approach."""
        g = GamePlayer.random(**kwargs, damage=1/2)
        self.group.newPlayer(g)
        self.group.active = True
        return g

    def updateWon(self):
        """Must be overloaded in order to change the won state of the level."""
        pass

    def showWin(self, context):
        """Called when the game is won."""
        context.console("Congratulations! You have won the game!", color=mycolors.YELLOW)
        self.logging_win = False

    def update(self):
        super().update()
        self.updateWon()
        self.checkWon()

    def checkWon(self):
        if self.won:
            if self.won_time is None:
                self.won_time = time.time()
                self.logging_win = True
            else:
                if time.time() - self.won_time > self.won_duration:
                    self.on = False


class DestroyAsteroids(AsteroidLevel):
    """Level in which the players must destroy all the asteroids to win."""

    def __init__(self, n=10, **kwargs):
        spaceships = ShooterGroup(active=False)
        missiles = MissileGroup()
        asteroids = AsteroidGroup.random(n=n, sparse=100)
        group = AsteroidGameGroup(spaceships, missiles, asteroids)
        super().__init__(group, **kwargs)
        self.asteroids_left = None

    def start(self):
        super().start()
        self.asteroids_left = 0

    def show(self, context):
        super().show(context)
        if self.asteroids_left != len(self.group.asteroids):
            self.asteroids_left = len(self.group.asteroids)
            context.console("{} asteroids left".format(self.asteroids_left))

    def updateWon(self):
        self.won = (len(self.group.asteroids) == 0)


class DestroySpaceShips(AsteroidLevel):
    """Level in which the players must kill themselves to win."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.spaceships_left = 0

    def start(self):
        super().start()
        self.spaceships_left = 0

    def show(self, context):
        super().show(context)
        if self.spaceships_left != len(self.group.spaceships):
            self.spaceships_left = len(self.group.spaceships)
            context.console("{} spaceships left".format(self.spaceships_left-1))

    def updateWon(self):
        self.won = (len(self.group.spaceships) == 0)


class DestroyShooters(DestroySpaceShips):
    def __init__(self, n=10, **kwargs):
        spaceships = ShooterGroup.random(n=n)
        missiles = MissileGroup()
        asteroids = AsteroidGroup()
        group = AsteroidGameGroup(spaceships, missiles, asteroids)
        super().__init__(group, **kwargs)


class DestroyHunters(DestroySpaceShips):
    def __init__(self, n=10, **kwargs):
        spaceships = HunterGroup.random(n=n)
        missiles = MissileGroup()
        asteroids = AsteroidGroup()
        group = AsteroidGameGroup(spaceships, missiles, asteroids)
        super().__init__(group, **kwargs)

    def update(self):
        super().update()
        self.group.spaceships.target = self.group.spaceships[0]


if __name__ == "__main__":
    from mymanager import GameManager
    game = SoloAsteroidGame()
    m = GameManager(game, controller=[0, 0])
    m()
