from myminimax import Minimax
from player import Player

from copy import deepcopy
from random import choice

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
        tree=self.treePlay(board.grille,self.side)
        if self.container(tree):
            minimax=Minimax(tree,start=0)
            result=minimax()
        else:
            result=None
        if result is not None:
            return board.mouvements[result]
        else:
            return choice(board.mouvements)


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
        result=self.evaluate(grid,side)
        return result

    def evaluate(self,grid,side):
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
