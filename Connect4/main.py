from pygame.locals import *
import pygame
import random
import copy

class Color:
    blue   = (  0,  0,255)
    red    = (255,  0,  0)
    yellow = (255,255,  0)
    black  = (  0,  0,  0)
    white  = (255,255,255)

class Token:
    yellow = 1
    red = -1
    empty = 0

done = False
won = False

class Window:
    def __init__(self, size=(700, 600)):
        self.size = size
        pygame.init()
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Puissance 4")
        self.font = pygame.font.Font('freesansbold.ttf', 50) 
        
    def tell(self, message, text_color, background_color):
        w, h = self.size
        surface = self.font.render(message, False, text_color, background_color) 
        rect = surface.get_rect()
        rect.center = (w//2, h//2) 
        self.screen.blit(surface, rect)
        pygame.display.flip()

class Board:
    class ColumnFull(Exception):
        pass
    def __init__(self, size=(7, 6)):
        self.size = (w, h) = size
        self.grid = [[0 for y in range(h)] for x in range(w)]
        self.won = False
        self.full = False
        self.borders = 1

    def __contains__(self, position):
        w, h = self.size
        x, y = position
        return 0<=x<w and 0<=y<h

    def show(self, window):
        wx, wy = window.size
        bx, by = self.size
        b = self.borders
        w = wx//bx-b
        h = wy//by-b
        for ix in range(bx):
            for iy in range(by):
                if self.grid[ix][iy]==Token.yellow:
                    color = Color.yellow
                elif self.grid[ix][iy]==Token.red:
                    color = Color.red
                else:
                    color = Color.blue
                x = int(ix*wx/bx)
                y = int(iy*wy/by)
                pygame.draw.rect(window.screen, color, (x,y,w,h), 0)

    def update_full(self):
        for column in self.grid:
            if Token.empty in column:
                return
        self.full = True

    def update_won(self):
        w, h = self.size
        for y in range(6):
            for x in range(4):
                if self.grid[x][y]==self.grid[x+1][y]==self.grid[x+2][y]==self.grid[x+3][y]!=Token.empty:
                    self.won = True
                    return
        for y in range(3):
            for x in range(7):
                if self.grid[x][y]==self.grid[x][y+1]==self.grid[x][y+2]==self.grid[x][y+3]!=Token.empty:
                    self.won = True
                    return
        for y in range(3):
            for x in range(4):
                if self.grid[x][y]==self.grid[x+1][y+1]==self.grid[x+2][y+2]==self.grid[x+3][y+3]!=Token.empty:
                    self.won = True
                    return
                if self.grid[x+3][y]==self.grid[x+2][y+1]==self.grid[x+1][y+2]==self.grid[x][y+3]!=Token.empty:
                    self.won = True
                    return

    def insert(self, choice, token):
        ix = choice
        if Token.empty in self.grid[ix]:
            for iy in reversed(range(self.size[1])):
                if self.grid[ix][iy] == Token.empty:
                    self.grid[ix][iy] = token
                    break
        else:
            raise Board.ColumnFull

class Game:
    tokens = [Token.yellow, Token.red]
    def __init__(self, players, board=Board(), window=Window()):
        self.players = players
        self.window = window
        self.board = board
        self.mouse = None
        self.clicking = False
        self.done = False
        self.turns = 0

    def main(self):
        self.show()
        while not self.done:
            self.update()
            self.play()
        pygame.quit()

    def show(self):
        self.window.screen.fill(Color.black)
        self.board.show(self.window)
        pygame.display.flip()

    def reset(self):
        self.board = Board()

    def update(self):
        wx, wy = self.window.size
        bx, by = self.board.size
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            elif event.type == MOUSEBUTTONDOWN:
                self.mouse = int(bx*event.pos[0]/wx), int(by*event.pos[1]/wy)
                self.clicking = True
            elif event.type == KEYDOWN:
                if event.key==K_q or event.key == K_ESCAPE:
                    self.done = True
                elif event.key==K_SPACE:
                    self.reset()
                    self.show()

    def play(self):
        if self.board.full or self.board.won:
            return
        turn = self.turns%2
        player = self.players[turn]
        token = Game.tokens[turn]
        if isinstance(player, Human):
            if not self.clicking:
                return
            self.clicking = False
            choice = player.play(self.mouse)
        elif isinstance(player, Bot):
            choice = player.play(self.board, token)
        try:
            self.board.insert(choice, token)
        except Board.ColumnFull:
            self.window.tell("La colonne est pleine.", Color.white, Color.red)
            return
        self.board.update_full()
        self.board.update_won()
        self.turns += 1
        self.show()
        if self.board.full or self.board.won:
            self.end()

    def end(self):
        last_token = Game.tokens[(self.turns-1)%2]
        if self.board.won:
            if last_token==Token.red:
                self.window.tell("Red wins", Color.red, Color.blue)
            else: # and yellow
                self.window.tell("Yellow wins", Color.yellow, Color.blue)
        else:
            self.window.tell("No one wins", Color.white, Color.blue)

class Metric:
    pass


class Victory(Metric):
    """Measures victories in a game."""

class Liberty(Metric):
    def __init__(self):
        self.directions = [(x, y) for x in [-1,0,1] for y in [-1,0,1] if not x==y==0]

    def __call__(self, grid, token):
        positions = self.player_positions(grid, token)
        s = sum(self.is_free_or_me(grid, token, *position) for position in positions)
        return s

    def player_positions(self, grid, token):
        positions = []
        w, h = len(grid), len(grid[0])
        for x in range(w):
            for y in range(h):
                if grid[x][y] == token:
                    positions.append((x, y))
        return positions

    def is_free(self, grid, x, y):
        w, h = len(grid), len(grid[0])
        n = 0
        for dx, dy in self.directions:
            if 0<=x+dx<w and 0<=y+dy<h:
                case = grid[x+dx][y+dy]
                if case == Token.empty:
                    n += 1
        return n

    def is_free_or_me(self, grid, token, x, y):
        w, h = len(grid), len(grid[0])
        n = 0
        for dx, dy in self.directions:
            if 0<=x+dx<w and 0<=y+dy<h:
                case = grid[x+dx][y+dy]
                if case == Token.empty or case == token:
                    n += 1
        return n

class LineLiberty(Metric):
    def value_grid(self, grid):
        pass
    def value_line(self, line):
        pass



class Player:
    pass

class Human(Player):
    def play(self, mouse):
        choice = mouse[0]
        return choice

class Bot(Player):
    def play(self, board, token):
        pass

class DumbBot(Bot):
    def play(self, board, token):
        w = board.size[0]
        choice = random.randint(0,w-1)
        return choice

class CleverBot(Bot):
    def __init__(self, max_level=5, metric=Liberty()):
        self.max_level = max_level
        self.metric = metric

    def play(self, board, token):
        return self.minimax(board.grid, token)

    def minimax(self, grid, token, level=1):
        """Minimax."""
        if level == self.max_level:
            return self.metric(grid, token)
        choice = 0; max_value = 0
        for ix,column in enumerate(grid):
            if column.count(Token.empty)>0:
                grid_ = copy.deepcopy(grid)
                grid_ = self.insert(grid_, ix, token)
                value = self.minimax(grid_, -token, level+1)
                if value>max_value:
                    max_value = value
                    choice = ix
        return choice
    
    def insert(self, grid, ix, token):
        for iy in reversed(range(len(grid[ix]))):
            if grid[ix][iy]==Token.empty:
                grid[ix][iy] = token
                break
        return grid

def main():
    players = [Human(), CleverBot()]
    game = Game(players)
    game.main()

if __name__ == '__main__':
    main()


import sys

def deep_getsizeof(o, ids=set()):
    d = deep_getsizeof
    if id(o) in ids:
        return 0
    r = sys.getsizeof(o)
    ids.add(id(o))
    if isinstance(o, str) or isinstance(0, unicode):
        return r
    if isinstance(o, Mapping):
        return r + sum(d(k, ids) + d(v, ids) for k, v in o.iteritems())
    if isinstance(o, Container):
        return r + sum(d(x, ids) for x in o)
    return r