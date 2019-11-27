from myspaceshipgroup import AsteroidGameGroup, GamePlayer, \
    AsteroidGroup, MissileGroup, ShooterGroup, HunterGroup, \
    SuperSpaceShipGroup, PlayerGroup
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
                player.respawn()

    def start(self):
        self.level.start()


class AsteroidLevel(Level):
    """Base class of all asteroid levels."""
    def __init__(self, *args, **kwargs):
        """Create an asteroid level."""
        super().__init__(*args, **kwargs)
        self.dt = 0.05
        self.rectangle = Rectangle((0, 0), (200, 200))
        self.logging_win = False
        self.won_time = None
        self.won_duration = 3

    def start(self):
        pass

    def restart(self, *args, **kwargs):
        # self.__dict__ = (super().__init__(*args, **kwargs)).__dict__
        # pass
        print("can not restart yet")

    def show(self, context):
        super().show(context)
        self.group.showBorn(context)
        self.rectangle.show(context)
        if self.logging_win:
            self.showWin(context)

    def newPlayer(self, **kwargs):
        """For now we are adding the base class of a player, but this is a naive approach."""
        g = GamePlayer.random(**kwargs)
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
        """Update the level by updating the groups and checking if the game is won.."""
        super().update()
        self.updateWon()
        self.checkWon()

    def checkWon(self):
        """Determine if the level is on or if the victory must be shown when the game is won."""
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
        """Create a level by creating the groups."""
        spaceships = SuperSpaceShipGroup(PlayerGroup(GamePlayer.random()))
        missiles = MissileGroup()
        asteroids = AsteroidGroup.random(n=n, sparse=100)
        group = AsteroidGameGroup(spaceships, missiles, asteroids)
        super().__init__(group, **kwargs)
        self.asteroids_left = None

    def start(self):
        """Start the game with 0 asteroids left."""
        super().start()
        self.asteroids_left = 0

    def restart(self, n):
        """Restart the game by respawning the asteroids."""
        self.group.asteroids = AsteroidGroup.random(n=n, sparse=100)
        self.asteroids_left = len(self.group.asteroids)

    def show(self, context):
        """Show the level and the number of asteroids left to destroy."""
        super().show(context)
        if self.asteroids_left != len(self.group.asteroids):
            self.asteroids_left = len(self.group.asteroids)
            context.console("{} asteroids left".format(self.asteroids_left))

    def updateWon(self):
        """Determine if the game is won depending on the number of asteroids of the group."""
        self.won = (len(self.group.asteroids) == 0)


class DestroySpaceShips(AsteroidLevel):
    """Level in which the players must kill themselves to win."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.spaceships_left = 0

    def start(self):
        """Start the level with 0 spaceships left."""
        super().start()
        self.spaceships_left = len(self.group.spaceships)

    def show(self, context):
        """Show the level with the number of spaceships left to destroy."""
        super().show(context)
        if self.spaceships_left != len(self.group.spaceships):
            self.spaceships_left = len(self.group.spaceships)
            context.console("{} spaceships left".format(self.spaceships_left-1))

    def updateWon(self):
        self.won = (len(self.group.spaceships) == 0)


class DestroyShooters(DestroySpaceShips):
    """Level in which the goal is to destroy all shooters."""
    # For now it is unclear how to use shooters that are not hunters.
    def __init__(self, n=10, **kwargs):
        """Create the level by creating the groups."""
        spaceships = ShooterGroup.random(n=n)
        missiles = MissileGroup()
        asteroids = AsteroidGroup()
        group = AsteroidGameGroup(spaceships, missiles, asteroids)
        super().__init__(group, **kwargs)


class DestroyHunters(DestroySpaceShips):
    """Level in which the goal is to destroy all hunters."""
    def __init__(self, n=10, **kwargs):
        """Create the level by creating the groups."""
        # AdvancedSpaceShip()
        spaceships = HunterGroup.random(n=n)
        missiles = MissileGroup()
        asteroids = AsteroidGroup()
        group = AsteroidGameGroup(spaceships, missiles, asteroids)
        super().__init__(group, **kwargs)

    def update(self):
        """Update the level and the targets."""
        super().update()
        self.group.spaceships.retarget(self.group.spaceships[0])


if __name__ == "__main__":
    from mymanager import GameManager
    game = SoloAsteroidGame()
    game.start()
    m = GameManager(game, controller=[0, 0, 0])
    m()
