import pygame

from mycolors import *
from mywindow import *
from mymoves import *
from mycontrols import *

class Player:
    def __init__(self,picture_directory,spawn_position):
        self.picture=pygame.image.load(picture_directory)
        self.spawn_position=spawn_position
        self.color=RED
        self.spawn()

    def spawn(self):
        self.position=self.spawn_position
        self.velocity=[0,0]
        self.acceleration=[0,1]

    def control(self):
        vx,vy=self.velocity
        keys=pygame.key.get_pressed()
        k=1
        if keys[K_UP]:
            vy=-1
        if keys[K_DOWN]:
            vy=1
        if keys[K_LEFT]:
            vx=-1
        if keys[K_RIGHT]:
            vx=1
        self.velocity=vx,vy
        print(self.velocity)

    def blockCollider(self,map):
        x,y=self.position
        X,Y=int(x),int(y)
        if map.grid[y-1][x].collision or map.grid[y-1][x+1].collision:
            self.velocity[1]=0


    def update(self,game):
        self.control()
        self.move()
        self.blockCollider(game.map)

    def move(self):
        x,y=self.position
        vx,vy=self.velocity
        ax,ay=self.acceleration
        vx+=ax
        vy+=ay
        x+=vx
        y+=vy
        self.position=[x,y]
        self.velocity=[vx,vy]

    def show(self,window):
        x,y=self.position
        wsx,wsy=window.size
        cx=x*wsx/20
        cy=y*wsy/20
        csy=wsy/20
        csx=wsx/20
        texture=pygame.transform.scale(self.picture, (csx, csy))
        window.screen.blit(texture, (cx,cy))
