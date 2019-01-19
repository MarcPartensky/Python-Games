import pygame
import os

class Block:
    def __init__(self,picture_directory,collision=True):
        self.collision=collision
        picture = pygame.image.load(picture_directory)
        self.picture=picture

    def show(self,window,coordonates):
        cx,cy,csx,csy=coordonates
        texture=pygame.transform.scale(self.picture, (csx, csy))
        window.screen.blit(texture, (cx,cy))
