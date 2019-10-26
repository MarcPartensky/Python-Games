from pygame.locals import *

from mywindow import Window

import numpy as np
import itertools
import mycolors
import random
import pygame
import copy
import time


class Player:
    """
        Base class of any TicTacToe player.

        Note:
         The functions getChoices and outcome are necessary eventhough the
         tictactoe object already have a getChoices and an outcome methods
         because it is more efficient and uses less memory which can be useful
         for recursive functions that need a lot of functions' calls.
    """

    def __str__(self):
        """Return a string representation of the player."""
        return self.name

    def choose(self, tictactoe, choice):
        """Choose a choice."""
        tictactoe.place(choice)
        tictactoe.update()

    def play(self, tictactoe):
        """Play by making its own decisions."""
        raise Exception("You implement this method to use it.")

    def getChoices(self, grid):
        """Return the choices that are available for a given grid."""
        return [(x, y) for x in range(3) for y in range(3) if grid[x][y] == 0]

    def outcome(self, g):
        """Return the outcome of the game of the given grid."""
        if g[0][0] == g[1][0] == g[2][0] and g[0][0] != 0:
            return g[0][0]
        if g[0][1] == g[1][1] == g[2][1] and g[0][1] != 0:
            return g[0][1]
        if g[0][2] == g[1][2] == g[2][2] and g[0][2] != 0:
            return g[0][2]
        if g[0][0] == g[0][1] == g[0][2] and g[0][0] != 0:
            return g[0][0]
        if g[1][0] == g[1][1] == g[1][2] and g[1][0] != 0:
            return g[1][0]
        if g[2][0] == g[2][1] == g[2][2] and g[2][0] != 0:
            return g[2][0]
        if g[0][0] == g[1][1] == g[2][2] and g[0][0] != 0:
            return g[0][0]
        if g[0][2] == g[1][1] == g[2][0] and g[0][2] != 0:
            return g[0][2]
        return 0

    def choose(self, g, c, p):
        """Return the grid after making a choice."""
        ng = copy.deepcopy(g)
        ng[c[0]][c[1]] = p
        return ng


class Human(Player):
    """Base class of any human player."""

    def __init__(self, name="Human"):
        """Create a human."""
        self.name = name
        self.chooser = True


class Robot(Player):
    """Base class of any robot player."""

    def __init__(self, name="Robot"):
        """Create a robot."""
        self.name = name
        self.chooser = False


class RandomRobot(Robot):
    """Robot that plays randomly."""

    def __init__(self, name="RandomRobot"):
        """Create a random player."""
        super().__init__(name)

    def play(self, tictactoe):
        """Play randomly."""
        return random.choice(tictactoe.choices)


class ProRobot(Robot):
    """Robot that always makes the best possible choice."""

    def __init__(self, name="ProRobot"):
        """Create a random player."""
        super().__init__(name)

    def play(self, tictactoe):
        """Play randomly."""
        m = self.bestMove(tictactoe.grid, tictactoe.token)
        return m[0]

    def bestMove(self, g, p):  # Super Minimax specially adapted for morpions
        """Return the best possible move."""
        choices = self.getChoices(g)
        if len(choices) == 1:
            w = self.outcome(self.choose(g, choices[0], p))
            return (choices[0], w)
        else:
            moves = []
            for choice in choices:
                ng = self.choose(g, choice, p)
                w = self.outcome(ng)
                if w == p:
                    # We already won, so it's needless to compute further
                    return (choice, w)
                moves.append(self.bestMove(ng, -p))
            # We use the fact that p equals 1 or -1
            m = max(moves, key=lambda x: p * x[1])
            return [choices[moves.index(m)], m[1]]


class TicTacToe:
    """TicTacToe game (that can be shown)."""

    @classmethod
    def create(cls):
        """Create a new game of TicTacToe."""
        pass
        return cls()

    @classmethod
    def createRandom(cls):
        """Create a game with a random grid."""
        grid = np.random.randint(-1, 2, (3, 3), dtype=int)
        return cls(grid)

    def __init__(self, grid=np.zeros((3, 3), dtype=int),
                 grid_color=mycolors.WHITE,
                 cross_color=mycolors.BLUE,
                 circle_color=mycolors.RED):
        """Create a game of TicTacToe using a given grid."""
        self.grid = grid
        self.state = 0
        self.tokens = [-1, 1]  # This cannot be changed
        self.grid_color = grid_color
        self.cross_color = cross_color
        self.circle_color = circle_color

    def restart(self):
        """Restart the tictactoe game."""
        self.grid = np.zeros((3, 3), dtype=int)
        self.state = 0

    def update(self):
        """Update the game."""
        if self:
            self.state += 1

    def put(self, choice, token):
        """Put a given token at a given choice."""
        x, y = choice
        self.grid[x][y] = token

    def select(self, choice):
        """Choose a choice."""
        self.put(choice, self.token)
        self.update()

    def choose(self, choice):
        """Try to make a choice but checks if it is valid to make it."""
        if self.available(choice):
            self.select(choice)

    def show(self, window):
        """Show the tictactoe."""
        self.showGrid(window)
        self.showObjects(window)

    def showGrid(self, window):
        """Show the grid."""
        w, h = window.size
        sx, sy = self.size
        x, y = w // sx, h // sy
        def line(p1, p2): window.draw.line(
            window.screen, self.grid_color, p1, p2)
        line((x, 0), (x, h))
        line((2 * x, 0), (2 * x, h))
        line((0, y), (w, y))
        line((0, 2 * y), (w, 2 * y))

    def showObjects(self, window):
        """Show the objects."""
        sx, sy = self.size
        for x in range(sx):
            for y in range(sy):
                if self.grid[x][y] == -1:
                    self.showCross(window, (x, y))
                elif self.grid[x][y] == 1:
                    self.showCircle(window, (x, y))

    def showCross(self, window, position):
        """Show a cross."""
        def line(p1, p2): window.draw.line(
            window.screen, self.cross_color, p1, p2)
        w, h = window.size
        sx, sy = self.size
        x, y = position
        ox, oy = w / (3 * sx), h / (3 * sy)
        rx, ry = w * (x + 1 / 2) / sx, h * (y + 1 / 2) / sy
        line((rx - ox, ry - oy), (rx + ox, ry + oy))
        line((rx - ox, ry + oy), (rx + ox, ry - oy))

    def showCircle(self, window, position):
        """Show a circle."""
        w, h = window.size
        x, y = position
        sx, sy = self.size
        rx, ry = int(w * (x + 1 / 2) / sx), int(h * (y + 1 / 2) / sy)
        ox, oy = w // (3 * sx), h // (3 * sy)
        r = min(ox, oy)
        window.draw.circle(window.screen, self.circle_color, (rx, ry), r)

    def available(self, position):
        """Determine if a position is available."""
        if position is not None:
            x, y = position
            return self.grid[x][y] == 0

    @property
    def list(self):
        return list(np.reshape(self.grid, (1, 9))[0])

    @property
    def choices(self):
        return [(x, y) for x in range(3) for y in range(3) if self.grid[x][y] == 0]

    @property
    def size(self):
        return (len(self.grid[0]), len(self.grid))

    @property
    def turn(self):
        return self.state % 2

    @property
    def token(self):
        return self.tokens[self.turn]

    @property
    def outcome(self):
        """Determine the outcome of a game i.e. who wins."""
        if self.grid[0][0] == self.grid[1][0] == self.grid[2][0] and self.grid[0][0] != 0:
            return self.grid[0][0]
        if self.grid[0][1] == self.grid[1][1] == self.grid[2][1] and self.grid[0][1] != 0:
            return self.grid[0][1]
        if self.grid[0][2] == self.grid[1][2] == self.grid[2][2] and self.grid[0][2] != 0:
            return self.grid[0][2]
        if self.grid[0][0] == self.grid[0][1] == self.grid[0][2] and self.grid[0][0] != 0:
            return self.grid[0][0]
        if self.grid[1][0] == self.grid[1][1] == self.grid[1][2] and self.grid[1][0] != 0:
            return self.grid[1][0]
        if self.grid[2][0] == self.grid[2][1] == self.grid[2][2] and self.grid[2][0] != 0:
            return self.grid[2][0]
        if self.grid[0][0] == self.grid[1][1] == self.grid[2][2] and self.grid[0][0] != 0:
            return self.grid[0][0]
        if self.grid[0][2] == self.grid[1][1] == self.grid[2][0] and self.grid[0][2] != 0:
            return self.grid[0][2]
        return 0

    @property
    def filled(self):
        """Determine if the grid is filled."""
        return self.list.count(0) == 0

    def __bool__(self):
        """Determine if the game is over or not."""
        return not(self.outcome != 0 or self.filled)


class TicTacToeManager:
    """
       Game manager of the tictactoe.

       Note:
        Since a tictactoe game is just basically a grid, the manager must
        manage the course of the game and is responsible for the TicTacToe object
        its players, and visual informations.
    """

    @classmethod
    def createWithRandomRobots(cls, **kwargs):
        """Create a new game with players that play randomly."""
        players = [RandomRobot(), RandomRobot()]
        game = TicTacToe()
        return cls(game, players, **kwargs)

    @classmethod
    def createWithSamePlayersClass(cls, players_cls, **kwargs):
        """Create a new game with players that play randomly."""
        players = [players_cls(), players_cls()]
        game = TicTacToe()
        return cls(game, players, **kwargs)

    @classmethod
    def createWithPlayersClass(cls, player1_cls, player2_cls, **kwargs):
        """Create a new game with players that play randomly."""
        players = [player1_cls(), player2_cls()]
        game = TicTacToe()
        return cls(game, players, **kwargs)

    @classmethod
    def createWithPlayers(cls, players, **kwargs):
        """Create a new game with given players."""
        game = TicTacToe()
        return cls(game, players, **kwargs)

    def __init__(self, tictactoe, players,
                 window=Window(name="TicTacToe", size=(500, 500)),
                 restart_at_end=False,
                 telling=True):
        """Create a game of TicTacToe using the TicTacToe object."""
        self.tictactoe = tictactoe
        self.players = players
        self.window = window
        self.default_size = window.size
        self.restart_at_end = restart_at_end
        # =>Easier to manipulate than having nasty infinities to deal with
        self.choice = None
        self.on = False
        self.telling = telling
        self.start_duration = 1
        self.end_duration = 1
        self.start_time = None
        self.end_time = None
        self.game_number = 0

    def __call__(self):
        """Start the game."""
        self.start()
        while self.window:
            self.events()
            self.update()
            self.show()

    def start(self):
        """Start the game."""
        self.on = True
        self.start_time = time.time()
        self.game_number += 1

    def events(self):
        """Deal with the events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.window.open = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.window.open = False
                if event.key == K_SPACE:
                    self.restart()
                if event.key == K_f:
                    self.window.switch(self.default_size)
            if event.type == VIDEORESIZE:
                self.window.screen = pygame.display.set_mode(
                    (event.w, event.h), RESIZABLE)
            if event.type == MOUSEMOTION:
                pass
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                self.click(event.pos)

    def click(self, position):
        """React to a click at a given position."""
        w, h = self.window.size
        sx, sy = self.tictactoe.size
        rx, ry = position
        x, y = sx * rx // w, sy * ry // h
        if self.tictactoe.available((x, y)):
            self.choice = (x, y)

    def restart(self):
        """Restart the game."""
        self.tictactoe.restart()
        self.start()

    def update(self):
        """Update the game of TicTacToe."""
        # If the game is not over.
        if self.tictactoe:
            # If the player is human, the choice can only be detected by the game,
            # because the player has no responsibility over the window
            if self.player.chooser:
                choice = self.choice
                self.choice = None
            else:
                choice = self.player.play(self.tictactoe)
            self.tictactoe.choose(choice)
        else:
            if self.on:
                self.end_time = time.time()
                self.on = False
            if self.restart_at_end:
                if time.time() - self.end_time > self.end_duration:
                    self.restart()

    def show(self):
        """Show the game."""
        self.window.clear()
        self.tictactoe.show(self.window)
        if self.telling:
            self.tellIfStarted()
            self.tellIfEnded()
        self.window.flip()

    def tellIfStarted(self):
        """Tell messages to the player at the begining of a game."""
        if self.game_number == 1:
            self.welcome()
        else:
            self.tellGameNumber()

    def welcome(self):
        """Welcome the players."""
        t = time.time() - self.start_time
        d = self.start_duration
        if t < d:
            c = int(255 * (1 - (t / d)))
            self.window.alert("Welcome to TicTacToe", color=(c, c, c))

    def tellGameNumber(self):
        """Tell the game number to screen."""
        t = time.time() - self.start_time
        d = self.start_duration
        if t < d:
            c = int(255 * (1 - (t / d)))
            self.window.alert("Starting game number " + str(self.game_number))

    def tellIfEnded(self):
        """Tell messages if the games has ended."""
        self.congratulate()

    def congratulate(self):
        """Congratulate the winner."""
        if self.end_time:
            t = time.time() - self.end_time
            d = self.end_duration
            if t < d:
                c = int(255 * (1 - (t / d)))
                if not self.tictactoe:
                    if self.winner is not None:
                        self.window.alert(
                            "The winner is " + self.nameWinner(), color=(c, c, c))
                    else:
                        self.window.alert("Draw", color=(c, c, c))

    def nameWinner(self):
        """Name the winner in a clever way:
        If the players have the same name it will also tell the player's number."""
        p1, p2 = self.players
        name = self.winner.name
        if p1.name == p2.name:
            name += str(self.tictactoe.turn + 1)
        return name

    @property
    def player(self):
        """Return the current player."""
        return self.players[self.tictactoe.turn]

    @property
    def winner(self):
        if self.tictactoe.outcome != 0:
            return self.players[self.tictactoe.turn]


if __name__ == "__main__":
    player1 = RandomRobot("ta soeur de 5 ans")  # Human("Marc")
    player2 = ProRobot("ton daron")
    m = TicTacToeManager.createWithPlayers(
        [player1, player2], restart_at_end=True, telling=True)
    m()
