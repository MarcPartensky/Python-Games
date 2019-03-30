from mycolors import *

import pygame

class Piece:
    def __init__(self,side,position):
        self.name=self.id+str(self.instance%2+1)
        self.side=side
        self.position=position
        self.diagonals=[(1,1),(-1,1),(-1,-1),(1,-1)]
        self.L_diagonals=[(2,1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2),(2,-1)]
        self.left=[(-1,0)]
        self.right=[(1,0)]
        self.up=[(0,1)]
        self.down=[(0,-1)]
        self.vertical=self.up+self.down
        self.horizontal=self.left+self.right
        self.axis=self.horizontal+self.vertical
        self.moves=[]
        self.special_moves=[]
        self.state=0
        self.max_norm=10
        self.direct_kill=True

    def show(self,window,coordonnates,colors):
        if self.side==1:
            color=colors[0]
        else:
            color=colors[1]
        x,y,sx,sy=coordonnates
        sx,sy=int(sx),int(sy)
        picture=pygame.image.load(self.picture_directory)
        picture=pygame.transform.scale(picture,(sx+12,sy+4))
        picture=colorize(picture,reverseColor(color))
        window.screen.blit(picture, (x-6,y-2))
        picture=pygame.transform.scale(picture,(sx,sy))
        picture=colorize(picture,color)
        window.screen.blit(picture, (x,y))


    def __repr__(self):
        return self.name+" of side "+str(self.side)+" is in "+str(self.position)

class Pawn(Piece):
    instance=0
    def __init__(self,side,position):
        Pawn.instance+=1
        self.instance=Pawn.instance
        self.id="Pawn"
        Piece.__init__(self,side,position)
        self.vectors=self.up
        self.norm=1
        self.moves=(self.vectors,self.norm)
        #prise en passant a ajouter
        self.picture_directory="Pictures/pawn.png"
        self.direct_kill=False
        self.en_passant=[([(0,1)],Pawn,None,None), ([((-1,1),(0,0)),((1,1),(0,0))],True,False)]
        self.diagonal_kill=[([(0,1)],Pawn,None,None), ([((-1,1),(0,0)),((1,1),(0,0))],True,False)]
        self.value=1



class Tower(Piece):
    instance=0
    def __init__(self,side,position):
        self.instance=Tower.instance
        self.id="Tower"
        Piece.__init__(self,side,position)
        self.vectors=self.axis
        self.norm=self.max_norm
        self.moves=(self.vectors,self.norm)
        self.picture_directory="Pictures/tower.png"
        Tower.instance+=1
        self.value=4

class Bishop(Piece):
    instance=0
    def __init__(self,side,position):
        self.instance=Bishop.instance
        self.id="Bishop"
        Piece.__init__(self,side,position)
        self.vectors=self.diagonals
        self.norm=self.max_norm
        self.moves=(self.vectors,self.norm)
        self.picture_directory="Pictures/bishop.png"
        Bishop.instance+=1
        self.value=3

class Horse(Piece):
    instance=0
    def __init__(self,side,position):
        self.instance=Horse.instance
        self.id="Horse"
        Piece.__init__(self,side,position)
        self.vectors=self.L_diagonals
        self.norm=1
        self.moves=(self.vectors,self.norm)
        self.picture_directory="Pictures/horse.png"
        Horse.instance+=1
        self.value=3

class Queen(Piece):
    instance=0
    def __init__(self,side,position):
        self.instance=Queen.instance
        self.id="Queen"
        Piece.__init__(self,side,position)
        self.vectors=self.axis+self.diagonals
        self.norm=self.max_norm
        self.moves=(self.vectors,self.norm)
        self.picture_directory="Pictures/queen.png"
        Queen.instance+=1
        self.value=7

class King(Piece):
    instance=0
    def __init__(self,side,position):
        self.instance=King.instance
        self.id="King"
        Piece.__init__(self,side,position)
        self.vectors=self.axis+self.diagonals
        self.norm=1
        self.moves=(self.vectors,self.norm)
        #roc a ajouter
        #mouvements speciaux=[
        #((mouvements),Entity,self.state,entity.state),]
        self.picture_directory="Pictures/king.png"
        self.castling=[(self.horizontal,Tower,0,0), ([((2,0),(0,1)),((-2,0),(-1,0))],False,False)]
        self.special_moves=[self.castling]
        King.instance+=1
        self.value=1000
        self.check=False

"""
Structure des mouvements speciaux:
special_moves=[special_move, ...]
    special_move=(conditions,actions)
        conditions=(relative_positions,entity,self.state,entity.state)
            relative_positions=[relative_position, ...]
                relative_position=[0,0]
            entity=out/None/piece
            self.state=0/None
            entity.state=0/None
        actions=(moves,kill,transformation)
            moves=[move, ...]
                move=(self.move,entity.move)
                    self.move=[0,1]
                    entity.move=[0,1] #mouvement relatif au self
            kill=True/False
            transformation=True/False
"""
