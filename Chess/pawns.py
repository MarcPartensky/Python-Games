from mycolors import *

import pygame

class Pawn:
    def __init__(self,side,position):
        self.side=side
        self.position=position
        self.diagonals=[(1,1),(-1,1),(-1,-1),(1,-1)]
        self.L_diagonals=[( 2, 1), ( 1, 2), (-1,2), (-2,1), (-2,-1), (-1,-2), (1,-2), ( 2,-1)]
        self.left=[(0,-1)]
        self.right=[(0,1)]
        self.up=[(0,1)]
        self.down=[(0,-1)]
        self.vertical=self.up+self.down
        self.horizontal=self.left+self.right
        self.axis=self.horizontal+self.vertical
        self.moves=[]
        self.special_moves=[]
        self.state=0
        self.max_norm=10

    def show(self,window,coordonnates,colors):
        if self.side==1:
            color=colors[0]
        else:
            color=colors[1]
        x,y,sx,sy=coordonnates
        picture=pygame.image.load(self.picture_directory)
        picture=pygame.transform.scale(picture,(sx+12,sy+4))
        picture=colorize(picture,reverseColor(color))
        window.screen.blit(picture, (x-6,y-2))
        picture=pygame.transform.scale(picture,(sx,sy))
        picture=colorize(picture,color)
        window.screen.blit(picture, (x,y))

class Knight(Pawn):
    def __init__(self,side,position):
        Pawn.__init__(self,side,position)
        self.id="Knight"
        self.vectors=self.up
        self.norm=1
        self.moves=(self.vectors,self.norm)
        self.special_moves=[(0,2,self.twoSteps)]
        #prise en passant a ajouter
        self.picture_directory="Pictures/knight.png"

    def twoSteps(self,board):
        return self.state==0


class Tower(Pawn):
    def __init__(self,side,position):
        Pawn.__init__(self,side,position)
        self.id="Tower"
        self.vectors=self.axis
        self.norm=self.max_norm
        self.moves=(self.vectors,self.norm)
        self.picture_directory="Pictures/tower.png"

class Bishop(Pawn):
    def __init__(self,side,position):
        Pawn.__init__(self,side,position)
        self.id="Bishop"
        self.vectors=self.diagonals
        self.norm=self.max_norm
        self.moves=(self.vectors,self.norm)
        self.picture_directory="Pictures/bishop.png"

class Horse(Pawn):
    def __init__(self,side,position):
        Pawn.__init__(self,side,position)
        self.id="Horse"
        self.vectors=self.L_diagonals
        self.norm=1
        self.moves=(self.vectors,self.norm)
        self.picture_directory="Pictures/horse.png"

class Queen(Pawn):
    def __init__(self,side,position):
        Pawn.__init__(self,side,position)
        self.id="Queen"
        self.vectors=self.axis
        self.norm=self.max_norm
        self.moves=(self.vectors,self.norm)
        self.picture_directory="Pictures/queen.png"

class King(Pawn):
    def __init__(self,side,position):
        Pawn.__init__(self,side,position)
        self.id="King"
        self.vectors=self.axis
        self.norm=1
        self.moves=(self.vectors,self.norm)
        #roc a ajouter
        self.picture_directory="Pictures/king.png"
