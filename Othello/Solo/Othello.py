from mywindow import *
from mycolors import *

from board import *
from player import *

import time
import pygame
from pygame.locals import *

from copy import deepcopy as new

class Othello:
    def __init__(self):
        self.name="Othello"
        self.window=Window(self.name,[800,800])
        self.window.background_color=GREEN
        self.grid_color=BLACK
        self.pieces_color=[WHITE,BLACK]
        self.moves_color=RED
        self.theme=[self.grid_color,self.pieces_color,self.moves_color]
        self.board=Board(self.theme)
        self.players=[Human(0),Robot(1)]
        self.won=False
        self.state=0
        self.input=None

    def __call__(self):
        self.show()
        while self.window.open and not self.won:
            self.window.check()
            self.getInput()
            self.update()
            self.show()
        self.finalScene()

    def finalScene(self):
        self.show()
        turn=self.state%2
        player=self.players[turn]
        if self.won:
            message="Player"+str(player.side+1)+" won!"
        else:
            message="Draw "
        position=list(self.window.centerText(message))
        position[0]-=50
        size=[int(len(message)*self.window.text_size/2.7),50]
        self.window.print(message,position,size,color=BLACK,background_color=WHITE)
        self.window.flip()
        while self.window.open:
            self.window.check()


    def getInput(self):
        input=self.input
        while (input is self.input) and self.window.open:
            self.window.check()
            click=self.window.click()
            cursor=self.window.point()
            input=(click,cursor)
        self.input=input

    def show(self):
        self.window.clear()
        self.board.show(self.window)
        self.window.flip()

    def update(self):
        self.board.check()
        if not self.board.won:
            turn=self.state%2
            player=self.players[turn]
            self.board.moves=self.board.getMoves(player.side,self.window)
            if len(self.board.moves)==0:
                #print(self.board.moves)
                self.state+=1
            else:
                player.play(self.input,new(self.board),self.window)
                if player.choice is not None:
                    x,y=player.choice
                    self.board.grid[y][x]=player.side+1
                    self.board.conquer(player.choice,player.side)
                    player.choice=None
                    self.state+=1
        else:
            self.won=True

if __name__=="__main__":
    game=Othello()
    game()
