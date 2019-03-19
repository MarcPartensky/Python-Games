"""
################################################################################
#
#              Institut Supérieur d'électronique de Paris (ISEP)
#
#                               SUJET DE TIPE:
#                     Othello et Intelligence Artificielle
#
#    Première année  --  MPSI
#
#    Créateurs : Marc  PARTENSKY
#                Valentin  COLIN
#                Alexandre Bigot
#
#    Version : 2019
#              1.1
#
###############################################################################
#
#                           SOMMAIRE de Player
#
#    note : commenter le script correctement
#
#    0. __init__   ................................................ ligne
#
###############################################################################
#
#                           SOMMAIRE de Human
#
#    0. __init__   ................................................ ligne
#    1. old_jouer   ............................................... ligne
#    2. jouer   ................................................... ligne
#
###############################################################################
#
#                           SOMMAIRE de Robot
#
#    0. __init__   ................................................ ligne
#    1.jouer   ................................................... ligne
#    2. main   .................................................... ligne
#
###############################################################################
"""
# --coding:utf-8--

from copy import deepcopy

import time
import random
import json
#import ia
import config as cfg
import pygame
#

class Player:
    def __init__(self):
        self.choix=None

class Humain(Player):
    def __init__(self):
        Player.__init__(self)


    def old_jouer(self,input,board,fenetre,side):
        click,cursor=input
        if click:
            position=board.adjust(cursor,fenetre)
            if board.estDansGrille(position):
                if position in board.mouvements:
                    self.choix=position
        return self.choix

    def jouer(self,plateau,fenetre,side):
        while fenetre.open:
            fenetre.check()
            if bool(pygame.mouse.get_pressed()[0]):
                position=plateau.adjuster(fenetre.point(),fenetre)#Donne des coordonnées
                if plateau.estDansGrille(position):
                    if position in plateau.mouvements:#On regarde si le clique est une possibilité propose par le plateau
                        self.choix=position
                        break
        return self.choix

class Robot(Player):
    def __init__(self):
        Player.__init__(self)

    def jouer(self,plateau,fenetre,side):
        return self.randomPlay(plateau)
        #return self.main(plateau)#todo verif si c'est bien possible

    def main(self, plateau):
        """"Methode à surchager"""
        pass

    def old_jouer(self,input,plateau,fenetre,side):
        return self.randomPlay(plateau)

    def randomPlay(self,board):
        self.choix=random.choice(board.mouvements)
        return self.choix



    def smartPlay(self,board):
        mouvements=board.mouvements
        for mouvement in mouvements:
            pass




















class Minimax:
    def __init__(self,tree,start=0,choice=None):
        self.start=start
        self.tree=tree
        self.choice=choice
        self.tree=self.rem_empty(self.tree)

    def decompose(self,object,n=0):
        if type(object) is list:
            decomposition=[]
            for x in object:
                decomposition.append(self.decompose(x,n+1))
            if n%2==self.start:
                value=max(decomposition)
            else:
                value=min(decomposition)
            self.choice=decomposition.index(value)
            return value
        else:
            return object

    def rem_none(self,l):
        if type(l) != list:
            return
        l[:] = [i for i in l if i is not []]
        for e in l:
            self.rem_none(e)

    def rem_empty(self,l):
        if type(l)==list: return [self.rem_empty(e) for e in l if e!=[]]
        else: return l


    def __call__(self):
        #print(self.tree)
        if self.tree!=[]:
            value=self.decompose(self.tree)
        return self.choice



class Beast(Player): #a ete rajoute pour faire des tests, ne sera pas present a la fin du projet
    def __init__(self,level=1):
        self.level=level
        self.advantage=[[ 9,-2, 1, 1, 1, 1,-2, 9],
                        [-2,-2,-1,-1,-1,-1,-2,-2],
                        [ 1,-1, 0, 0, 0, 0,-1, 1],
                        [ 1,-1, 0, 0, 0, 0,-1, 1],
                        [ 1,-1, 0, 0, 0, 0,-1, 1],
                        [ 1,-1, 0, 0, 0, 0,-1, 1],
                        [-2,-2,-1,-1,-1,-1,-2,-2],
                        [ 9,-2, 1, 1, 1, 1,-2, 9]]

    def jouer(self,board,window,side):
        self.board=board
        self.side=side
        #print("moves:",board.moves)
        tree=self.treePlay(board.grille,self.side)
        #print("mouvements:",board.mouvements)
        #print("tree:",tree)
        if self.container(tree):
            minimax=Minimax(tree,start=0)
            result=minimax()
        else:
            result=None
        #print("result:",result)
        if result is not None:
            #print("choix:",board.mouvements[result])
            return board.mouvements[result]
        else:
            return random.choice(board.mouvements)


    def treePlay(self,grid,side,level=0):
        if level>self.level:
            return self.reward(grid,side)
        else:
            tree=[]
            self.board.grille=grid
            moves=self.board.obtenirMouvementsValides(side)
            for move in moves:
                sub_grid=deepcopy(grid)
                x,y=move
                self.board.grille=sub_grid
                self.board.placerPion(move,side)
                tree.append(self.treePlay(self.board.grille,(side+1)%2,level+1))
            return tree

    def reward(self,grid,side):
        #return len(self.board.getMoves(grid,side,None))
        #print(grid,side)
        result=self.evaluate(grid,side)
        #print(result)
        return result

    def evaluate(self,grid,side):
        """sum=0
        for y in range(len(self.advantage)):
            for x in range(len(self.advantage[y])):
                factor=2*side-1
                #print("factor: ",factor)
                advantage=self.advantage[y][x]
                #print("advantage: ",advantage)
                value=int(grid[y][x]==1)-int(grid[y][x]==2)
                sum+=advantage*value*factor
        print("sum: ",sum)
        return sum"""

        #Does exactly the same thing but in one line ;)
        return sum([sum([(int(grid[y][x]==self.side)-int(grid[y][x]!=self.side and grid[y][x]>=0))*self.advantage[y][x] for x in range(len(self.advantage[y]))]) for y in range(len(self.advantage))])

    def container(self,tree):
        if type(tree)!=list:
            return True
        else:
            found=False
            for element in tree:
                if self.container(element):
                    found=True
                    break
            return found
