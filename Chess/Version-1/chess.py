from mywindow import *
from mycolors import *
#from myminimax import Minimax

from pieces import Piece,Horse,Bishop,Tower,Pawn,Queen,King
from board import Board
from player import Player
from human import Human
from robot import Robot

import json
import time
import pygame
from pygame.locals import *
import os


""" Plan:
Control: Game=>Player
              =>Board=>Piece=>Pieces
Game,Player: Active
Board,Piece,Pieces: Passive
"""

class Chess:
    def __init__(self):
        self.name="Chess"
        self.theme_mode=0
        self.loadThemes()
        self.window=Window(name=self.name,size=[700,700])
        self.player1=Human(1)
        self.player2=Robot(2)
        self.board=Board()
        self.delta=0.00000001
        self.cursor=None
        self.click=None
        self.player=self.player1

    def loadThemes(self):
        #Format=pieces_colors,grid_colors,selecters_colors
        self.pieces_colors_classic=[WHITE,BLACK]
        self.piece_colors_dark=[WHITE,BLACK]
        self.piece_colors_light=[WHITE,BLACK]
        self.piece_colors_random=[randomColor(),randomColor()]

        self.grid_colors_classic=[[BEIGE,LIGHTBROWN],BLACK]
        self.grid_colors_dark=[[DARKGREY,BLACK],WHITE]
        self.grid_colors_light=[[LIGHTGREY,WHITE],BLACK]
        self.grid_colors_random=[[randomColor() for i in range(2)],randomColor()]

        self.selecters_colors_classic=[[BEIGE,WHITE],[BEIGE,WHITE],[BEIGE,WHITE],[BEIGE,WHITE]]
        self.selecters_colors_dark=[[LIGHTGREY,BLACK],[WHITE,BLACK],[HALFGREY,BLACK],[DARKGREY,BLACK]]
        self.selecters_colors_light=[[GREY,WHITE],[BLACK,WHITE],[WHITE,BLACK],[GREY,WHITE]]
        self.selecters_colors_random=[[randomColor(),randomColor()] for i in range(4)]

        self.theme_classic=[self.pieces_colors_classic,self.grid_colors_classic,self.selecters_colors_classic]
        self.theme_dark=(self.piece_colors_dark,self.grid_colors_dark,self.selecters_colors_dark)
        self.theme_light=(self.piece_colors_light,self.grid_colors_light,self.selecters_colors_light)
        self.theme_random=(self.piece_colors_random,self.grid_colors_random,self.selecters_colors_random)

        self.themes=[self.theme_dark,self.theme_light,self.theme_classic,self.theme_random]

    def __call__(self):
        self.show()
        while self.window.open and not self.board.won:
            self.window.check()
            #print(self.board.moving)
            if isinstance(self.player,Human):
                self.input()
            else:
                if self.board.moving_shown and self.board.moving is not None:
                    self.board.updateMoving(self.window,self.theme)
            self.play()
            self.check()
            time.sleep(self.delta)
            self.show()

    def end(self):
        self.board.end()
        self.window.kill()

    def input(self):
        cursor=None
        self.updating=False
        while (not self.updating) and self.window.open:
            self.window.check()
            typing=False
            #print(self.board.moving_shown, self.board.moving)
            if self.board.moving_shown and self.board.moving is not None:
                #print("supposed to do something here")
                self.board.updateMoving(self.window,self.theme)
            cursor=self.cursor
            self.click=self.window.click()
            self.cursor=self.board.point(self.window)
            keys=pygame.key.get_pressed()
            if keys[K_RSHIFT] or keys[K_LSHIFT]:
                self.board.reverseMove()
                typing=True
            if keys[K_SPACE]:
                self.loadThemes()
                self.theme_mode=(self.theme_mode+1)%len(self.themes)
                typing=True
            if cursor==self.cursor and not self.click and not typing:
                self.updating=False
            else:
                self.updating=True

    def play(self):
        click=self.click
        position=self.cursor
        board=self.board #giving the player a copy of the board
        if board.state%2==0:
            self.player=self.player1
        else:
            self.player=self.player2
        self.player.play(board,position,click)
        if self.player.hasChosen:
            entity=board.piece_selecter
            move=board.move_selection
            position=board.locateByEntity(entity)
            moves=board.getMoves(entity,position)
            if entity is not None and move in moves: #Testing if player's choice is possible before changing the true board
                self.board.move(entity,position,move)
                self.board.updateHistoric()
                print(self.board.getPresentation(board.state,(entity,position,move)))
            self.player.hasChosen=False

    def check(self):
        self.player1.alive=self.board.isAlive("King",1)
        self.player2.alive=self.board.isAlive("King",2)
        if self.player1.alive and self.player2.alive:
            self.board.won=False
        else:
            self.board.won=True
            if self.player1.alive:
                self.board.winner=self.player1
            if self.player2.alive:
                self.board.winner=self.player2

    def show(self):
        self.theme=self.themes[self.theme_mode]
        #self.window.screen.fill(WHITE)
        self.board.show(self.window,self.theme)
        self.window.flip()

    def save(self):
        name="Chess"
        new_directory=directory+"/Games"
        os.chdir(new_directory)
        files=os.listdir()
        n=max([int(file[6]) for file in files]+[0])+1
        name+=" "+str(n)
        print(self.__dict__)
        self.window.__dict__
        del self.window
        del self.player1
        del self.player2
        del self.board
        with open(name+".json","w") as file:
            json.dump(self.__dict__,file)
        print(name)
        #with open():


if __name__=="__main__":
    directory=os.getcwd()
    print(directory)
    print("\n\n")
    game=Chess()
    game()
    game.save()
    game.end()
