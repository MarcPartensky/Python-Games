from copy import deepcopy

import random
import json

class Player:
    def __init__(self,side):
        self.choice=None
        self.side=side


class Robot(Player):
    def __init__(self,side):
        Player.__init__(self,side)

    def play(self,input,board,window):
        self.randomPlay(board)

    def randomPlay(self,board):
        self.choice=random.choice(board.moves)




    def smartPlay(self,board):
        moves=board.moves
        for move in moves:
            pass




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
