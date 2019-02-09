from mycolors import *

import pygame

class Pencil:
    def __init__(self,position=None,size=None,color=WHITE,form=0,radius=2,text_size=60,text_font="monospace",text_color=WHITE,points=[],clicking=False,width=0,connect=False,used=True):
        """Create pencil instance."""
        self.position=position
        self.size=size
        self.color=color
        self.form=form
        self.radius=radius
        self.text_font=text_font
        self.text_size=text_size
        self.points=points
        self.clicking=clicking
        self.used=used
        self.width=width

    def update(self,click,cursor):
        """Update update la fenetre"""
        self.clicking=click
        self.position=cursor


    def drawPoints(self,surface):
        """Draw all points using surface, points and colors."""
        for point in self.points:
            self.draw(surface,point,color)

    def draw(self,surface):
        """Draw objects on the surface using surface, position and color."""
        if self.form==0:
            pygame.draw.circle(surface,self.color,self.position,self.radius,self.width)
        if self.form==1:
            pygame.draw.rect(surface,self.color,list(self.position)+list(self.size),self.width)
        if self.form==2:
            pygame.draw.line(surface,self.color,self.position,self.size,self.width)
        if self.form==3:
            if len(self.points)>1:
                pygame.draw.lines(surface,self.color,self.connect,self.points,self.width)



"""
forms:
circle=0
rect=1
line=2
lines=3
triangle=4
"""
