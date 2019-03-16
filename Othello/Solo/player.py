from myminimax import Minimax

from board import Board

from copy import deepcopy as new

import random
import json

class Player:
    def __init__(self,side):
        self.choice=None
        self.side=side
    def randomPlay(self,board):
        self.choice=random.choice(board.moves)


class Robot(Player):
    def __init__(self,side,strategy):
        Player.__init__(self,side)
        self.strategy=strategy
        self.advantage=[[ 2,-2, 1, 1, 1, 1,-2, 2],
                        [-2,-2,-1,-1,-1,-1,-2,-2],
                        [ 1,-1, 0, 0, 0, 0,-1, 1],
                        [ 1,-1, 0, 0, 0, 0,-1, 1],
                        [ 1,-1, 0, 0, 0, 0,-1, 1],
                        [ 1,-1, 0, 0, 0, 0,-1, 1],
                        [-2,-2,-1,-1,-1,-1,-2,-2],
                        [ 2,-2, 1, 1, 1, 1,-2, 2]]

    def play(self,input,board,window):
        if self.strategy:
            self.smartPlay(board)
        else:
            self.randomPlay(board)



    def smartPlay(self,board):
        moves=board.moves
        choices=[[move,self.advantage[move[0]][move[1]]] for move in board.moves]
        self.choice=sorted(choices,key=lambda c:c[1],reverse=True)[0][0]
        #print("choice",self.choice)

    def smart1Play(self,board):
        moves=board.moves
        choices=[[move,self.advantage[move[0]][move[1]]] for move in board.moves]
        self.choice=sorted(choices,key=lambda c:c[1],reverse=True)[0][0]



class Beast(Player):
    def __init__(self,side,level=2):
        Player.__init__(self,side)
        self.level=level
        self.advantage=[[ 2,-2, 1, 1, 1, 1,-2, 2],
                        [-2,-2,-1,-1,-1,-1,-2,-2],
                        [ 1,-1, 0, 0, 0, 0,-1, 1],
                        [ 1,-1, 0, 0, 0, 0,-1, 1],
                        [ 1,-1, 0, 0, 0, 0,-1, 1],
                        [ 1,-1, 0, 0, 0, 0,-1, 1],
                        [-2,-2,-1,-1,-1,-1,-2,-2],
                        [ 2,-2, 1, 1, 1, 1,-2, 2]]

    def play(self,input,board,window):
        self.board=board
        #print("moves:",board.moves)
        tree=self.treePlay(board.grid,self.side,1)
        minimax=Minimax(tree)
        #print("tree:",minimax.tree)
        #print(minimax(),len(board.moves),len(tree))
        result=minimax()
        if result is not None:
            self.choice=board.moves[result]
        else:
            self.randomPlay(board)


    def treePlay(self,grid,side,level):
        if level>self.level:
            return self.reward(grid,side)
        else:
            tree=[]
            moves=self.board.getMoves(grid,side,None)
            for move in moves:
                sub_grid=new(grid)
                x,y=move
                sub_grid[y][x]=side+1
                self.board.conquer(sub_grid,move,side)
                tree.append(self.treePlay(sub_grid,(side+1)%2,level+1))
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
        return sum([sum([(2*side-1)*(int(grid[y][x]==1)-int(grid[y][x]==2))*self.advantage[y][x] for x in range(len(self.advantage[y]))]) for y in range(len(self.advantage))])









class Human(Player):
    def __init__(self,side):
        Player.__init__(self,side)


    def play(self,input,board,window):
        click,cursor=input
        if click:
            position=board.adjust(cursor,window)
            if board.inGrid(position):
                if position in board.moves:
                    self.choice=position

class Spectator:
    def __init__(self):
        pass
    def statistics(self,board):
        sx,sy=board.size
        with open("Statistic Grid.json","w") as file:
            object=json.load(file)
        object=json.loads(object)
        advantage=object["advantage"]
        for y in range(sy):
            for x in range(sx):
                pass
