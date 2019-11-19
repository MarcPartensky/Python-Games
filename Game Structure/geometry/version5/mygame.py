from myentitygroup import EntityGroup
from mymanager import Manager # Just to solve the deprecated complex manager class

import time


class ComplexGameManager(Manager):
    """A game is a manager that is specialized in game projects."""

    def __init__(self, levels, stage=0, speed=0.01, **kwargs):
        """Create a game using the list of levels and optional stage, speed and other arguments for the manager."""
        self.levels = levels
        self.stage = stage
        self.speed = speed
        self.t = time.time()
        super().__init__(**kwargs)

    def getLevel(self):
        return self.levels[self.stage]

    def setLevel(self, level):
        self.levels[self.stage] = level

    def delLevel(self):
        del self.levels[self.stage]

    level = property(getLevel, setLevel, delLevel)

    def show(self):
        """Show the current level of the game."""
        self.level.show(self.context)

    def update(self):
        """Update the current level if the time is right, so that the game speed
        does not depend on the efficiency of the computer."""
        if time.time() - self.t > self.speed:
            self.level.update(self.dt)
            self.t = time.time()

    def reactKeyDown(self, key):
        """Make all entities react to the keydown event."""
        super().reactKeyDown(key)
        self.level.reactKeyDown(key)

    def reactMouseMotion(self, position):
        """Make all entities react to the mouse motion."""
        position = self.context.getFromScreen(tuple(position))
        self.level.reactMouseMotion(position)

    def reactMouseButtonDown(self, button, position):
        """Make all entities react to the mouse button down event."""
        position = self.context.getFromScreen(tuple(position))
        self.level.reactMouseButtonDown(button, position)


class Game:
    def __init__(self, *levels, stage=0, speed=0.1):
        """Create a game using the list of levels and optional stage, speed and other arguments for the manager."""
        self.levels = list(levels)
        self.stage = stage
        self.speed = speed
        self.t = time.time()

    def getLevel(self):
        return self.levels[self.stage]

    def setLevel(self, level):
        self.levels[self.stage] = level

    def delLevel(self):
        del self.levels[self.stage]

    level = property(getLevel, setLevel, delLevel)

    def reactKeyDown(self, key):
        """Make all entities react to the keydown event."""
        self.level.reactKeyDown(key)

    def reactMouseMotion(self, position):
        """Make all entities react to the mouse motion."""
        self.level.reactMouseMotion(position)

    def reactMouseButtonDown(self, button, position):
        """Make all entities react to the mouse button down event."""
        self.level.reactMouseButtonDown(button, position)

    def update(self):
        self.level.update()

    def fixedUpdate(self):
        """Update the current level if the time is right, so that the game speed
        does not depend on the efficiency of the computer."""
        if time.time() - self.t > self.speed:
            self.level.update()
            self.t = time.time()

    def show(self, context):
        """Show the current level of the game."""
        self.level.show(context)

    def getPlayers(self):
        return self.level.players

    def setPlayers(self, players):
        self.level.players = players

    def delPlayers(self):
        self.level.players.clear()

    players = property(getPlayers, setPlayers, delPlayers)


class Level:
    def __init__(self, group, on=True, won=False, dt=0.01):
        """Create a level using the group of the level and optional the 'on' and 'won' parameters."""
        self.group = group
        self.on = on
        self.won = won
        self.dt = dt
        self.players = {}

    def update(self):
        self.group.update(self.dt)

    def show(self, context):
        self.group.show(context)

    def reactKeyDown(self, key):
        self.group.reactKeyDown(key)

    def reactMouseMotion(self, position):
        self.group.reactMouseMotion(position)

    def reactMouseButtonDown(self, button, position):
        self.group.reactMouseButtonDown(button, position)

    def control(self, controller):
        """Return the controlled entity using the controller."""
        return self.group.control(controller)


class DuoBattle(Level):
    """2 Fighters 1 winner:
    A Duo Battle is level which contains 2 entities which must fight to win the level."""

    def __init__(self, entity1, entity2):
        """Create a duo battle using 2 entities.
        It better be entities that can shoot otherwise the game might not end soon."""
        group = BasicEntityGroup(entity1, entity2)
        super().__init__(group)

    def update(self):
        self.group.update()


class Player:
    def __init__(self, game, control):
        """Create a player using its game and control."""
        self.game = game
        self.control = control
