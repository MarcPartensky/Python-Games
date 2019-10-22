#-------#
#Credits#
#-------#

__author__ = "Marc Partensky"
__license__ = "Marc Partensky Company"
__game__ = "Snake"

"""This game is available on every computer device that has Python installed."""

#------------#
#Dependencies#
#------------#

import random
import time
import math
import sys
import os

v=sys.version[:3]

try:
    import numpy as np
except:
    print("Installing numpy dependency.")
    os.system("pip"+v+" install numpy")
    import numpy as np

try:
    from pygame.locals import *
    import pygame
except:
    print("Installing pygame dependency.")
    os.system("pip"+v+" install pygame")
    from pygame.locals import *
    import pygame


#DIRECTORY=os.getcwd()
#print("Your current directory is:",DIRECTORY)
#os.chdir(DIRECTORY)

#---------#
#Variables#
#---------#

BLUE = (0,  0, 255)
RED = (255,  0,  0)
GREEN = (0, 255,  0)
YELLOW = (255, 255,  0)
BLACK = (0,  0,  0)
WHITE = (255, 255, 255)

RIGHT = 0
UP = 1
LEFT = 2
DOWN = 3

#-------#
#Classes#
#-------#


class Window:
    def __init__(self, background, title="Snake"):
        self.title = title
        self.opened = True
        pygame.init()
        info = pygame.display.Info()
        s = max(info.current_w // 2, info.current_h // 2)
        self.size = (s, s)
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.title)
        self.background = pygame.transform.scale(background, self.size)
        self.drawPicture(self.background, (0, 0))

    def direction(self):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            return LEFT
        if keys[K_RIGHT]:
            return RIGHT
        if keys[K_UP]:
            return UP
        if keys[K_DOWN]:
            return DOWN

    def check(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.opened = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.opened = False

    def select(self):
        while not self.closed():
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    return (event.pos[0], event.pos[1])

    def flip(self):
        pygame.display.flip()

    def drawPicture(self, picture, position):
        self.screen.blit(picture, position)

    def draw(self, color, coordonnates, size):
        x, y = coordonnates
        sx, sy = size
        pygame.draw.rect(self.screen, color, (x, y, sx, sy), 0)

    def kill(self):
        pygame.quit()


class Map:
    def __init__(self, background_directory, size=[20, 20], color_line=BLACK):
        self.size = size
        self.board = np.zeros(self.size)
        self.color_line = color_line
        self.background_directory = background_directory
        self.background = pygame.image.load(self.background_directory)

    def oldshow(self, window):
        window.screen.fill(self.color_background)
        mx, my = self.size
        wx, wy = window.size
        cx, cy = wx / mx, wy / my
        for x in range(mx):
            for y in range(my):
                window.draw(self.color_case, (cx * x + 1,
                                              cy * y + 1), (cx - 1, cy - 1))

    def show(self, window):
        mx, my = self.size
        wx, wy = window.size
        cx, cy = wx / mx, wy / my
        for x in range(mx):
            window.draw(self.color_line, (cx * x, 0), (1, wy))
        for y in range(my):
            window.draw(self.color_line, (0, cy * y), (wx, 1))


class Snake:
    def __init__(self, picture_directory, size=4):
        self.picture = pygame.image.load(picture_directory)
        self.size = size
        self.food_eaten = 0
        self.alive = False

    def loadTexture(self, map, window):
        mx, my = map.size
        wx, wy = window.size
        cx, cy = wx // mx, wy // my
        self.texture = pygame.transform.scale(self.picture, (cx, cy))

    def spawn(self, map):
        self.alive = True
        self.direction = random.randint(0, 3)
        mx, my = map.size
        self.head = [random.randint(
            0, mx - 1 - self.size), random.randint(0, my - 1 - self.size)]
        self.body = [self.head]
        x, y = self.head
        r = self.direction
        for i in range(self.size - 1):
            if r == LEFT:
                part = [x + i, y]
            if r == RIGHT:
                part = [x - i, y]
            if r == UP:
                part = [x, y + i]
            if r == DOWN:
                part = [x, y - i]
            self.body.append(part)
        self.tail = self.body[-1]

    def eat(self, food, map):
        self.food_eaten += 1
        self.body.append(self.tail)
        food.spawn(map)

    def move(self):
        x, y = self.head
        if self.direction == RIGHT:
            x += 1
        if self.direction == LEFT:
            x -= 1
        if self.direction == UP:
            y -= 1
        if self.direction == DOWN:
            y += 1
        self.head = [x, y]
        self.tail = self.body[-1]
        self.body = [self.head] + self.body[:-1]

    def bodyChanges(self):
        for part in self.body[1:]:
            if part == self.head:
                self.alive = False

    def borderChanges(self, map):
        x, y = self.head
        mx, my = map.size
        sx, sy = mx - 1, my - 1
        if x < 0:
            x = sx
        if x > sx:
            x = 0
        if y < 0:
            y = sy
        if y > sy:
            y = 0
        self.head = x, y

    def foodChanges(self, food, map):
        if self.head == food.coordonnates:
            self.eat(food, map)

    def show(self, map, window):
        mx, my = map.size
        wx, wy = window.size
        cx, cy = wx // mx, wy // my
        X, Y = self.head
        for part in self.body:
            x, y = part
            window.drawPicture(self.texture, (x * cx, y * cy))

    def opposite(self, direction):
        return direction == (self.direction + 2) % 4

    def lead(self, window):
        direction = window.direction()
        if direction is not None and not self.opposite(direction):
            self.direction = direction

    def play(self, map, window, food):
        self.lead(window)
        self.move()
        self.bodyChanges()
        self.borderChanges(map)
        self.foodChanges(food, map)

    def win(self, map):
        mx, my = map.size
        return (self.size == mx * my)


class Food:
    def __init__(self, picture_directory):
        self.picture = pygame.image.load(picture_directory)

    def loadTexture(self, map, window):
        mx, my = map.size
        wx, wy = window.size
        cx, cy = wx // mx, wy // my
        self.texture = pygame.transform.scale(self.picture, (cx, cy))

    def spawn(self, map):
        mx, my = map.size
        self.coordonnates = (random.randint(0, mx - 1),
                             random.randint(0, my - 1))

    def show(self, map, window):
        x, y = self.coordonnates
        mx, my = map.size
        wx, wy = window.size
        cx, cy = wx / mx, wy / my
        window.drawPicture(self.texture, (x * cx, y * cy))

#----------#
#Main class#
#----------#


class Game:
    def __init__(self):
        self.loadPictures()
        self.loadEntities()
        self.loadTextures()
        self.speed = 0.05
        self.main()

    def loadEntities(self):
        self.map = Map(self.background_directory)
        self.window = Window(self.map.background)
        self.snake = Snake(self.snake_body_picture)
        self.food = Food(self.food_picture)

    def loadPictures(self):
        self.background_directory = "Pictures/red space.jpg"
        self.snake_body_picture = "Pictures/snake.jpg"
        self.food_picture = "Pictures/potato.png"

    def loadTextures(self):
        self.snake.loadTexture(self.map, self.window)
        self.food.loadTexture(self.map, self.window)

    def show(self):
        self.window.drawPicture(self.window.background, (0, 0))
        self.map.show(self.window)
        self.food.show(self.map, self.window)
        self.snake.show(self.map, self.window)
        self.window.flip()

    def play(self):
        self.snake.spawn(self.map)
        self.food.spawn(self.map)
        self.show()
        while not self.snake.win(self.map) and self.window.opened and self.snake.alive:
            self.window.check()
            time.sleep(self.speed)
            self.snake.play(self.map, self.window, self.food)
            self.show()

    def main(self):
        while self.window.opened:
            self.play()
        self.window.kill()

#-------#
#Actions#
#-------#


game = Game()
