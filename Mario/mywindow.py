from mycolors import *

import pygame
from pygame.locals import *



class Window:
    made=0
    def __init__(self,game=None,size=None,font="monospace",text_color=BLACK,set=True):
        Window.made+=1
        self.number=Window.made
        self.title=game.name
        self.font=font
        self.open=True
        self.size=size
        self.text_color=text_color
        if set:
            self.set()

    def set(self):
        pygame.init()
        self.setSize()
        self.font = pygame.font.SysFont(self.font, 65)
        self.screen=pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.title)

    def setSize(self):
        if self.size is None:
            info = pygame.display.Info()
            self.size=(info.current_w/2,info.current_h/2)

    def pop_up(self,message):
        pass

    def scale(self,picture,size):
        return pygame.transform.scale(picture,size)

    def check(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.open=False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.open=False

    def direction(self):
        keys=pygame.key.get_pressed()
        if keys[K_LEFT]:
            return LEFT
        if keys[K_RIGHT]:
            return RIGHT
        if keys[K_UP]:
            return UP
        if keys[K_DOWN]:
            return DOWN

    def select(self):
        while self.open:
            self.check()
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    return (event.pos[0],event.pos[1])

    def point(self):
        for event in pygame.event.get():
            return (event.pos[0],event.pos[1])

    def flip(self):
        pygame.display.flip()

    def drawPicture(self,picture,position):
        self.screen.blit(picture, position)

    def display(page):
        pass
    def showText(self,text,position,color,font,size):
        font=pygame.font.SysFont(font, size)
        label = font.render(text, 1, color)
        self.screen.blit(label, position)
    def kill(self):
        pygame.quit()

print("mywindow imported")
