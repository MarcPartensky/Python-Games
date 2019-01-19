from mywindow import *
from mycolors import *

from pawns import *
from board import *
from player import *

import time
import pygame
from pygame.locals import *



""" Plan:
Control: Game=>Player
             =>Board=>Pawn=>Pawns
Game,Player: Active
Board,Pawn,Pawns: Passive
"""

class Chess:
    def __init__(self):
        self.name="Chess"
        self.theme_mode=0
        self.loadThemes()
        self.window=Window(self.name,[700,700])
        self.player1=Human(1)
        self.player2=Human(2)
        self.board=Board()
        self.delta=0.00000001
        self.cursor=None
        self.click=None
        self.session()

    def loadThemes(self):
        #Format=pawns_colors,grid_colors,selecters_colors
        self.pawns_colors_classic=[WHITE,BLACK]
        self.pawn_colors_pro=[WHITE,BLACK]
        self.pawn_colors_random=[randomColor(),randomColor()]

        self.grid_colors_classic=[[BEIGE,LIGHTBROWN],BLACK]
        self.grid_colors_pro=[[DARKGREY,BLACK],WHITE]
        self.grid_colors_random=[[randomColor(),randomColor()],randomColor()]

        self.selecters_colors_classic=[[BEIGE,WHITE],[BEIGE,WHITE]]
        self.selecters_colors_pro=[[LIGHTGREY,BLACK],[WHITE,BLACK]]
        self.selecters_colors_random=[[randomColor(),randomColor()],[randomColor(),randomColor()]]

        self.theme_classic=[self.pawns_colors_classic,self.grid_colors_classic,self.selecters_colors_classic]
        self.theme_pro=(self.pawn_colors_pro,self.grid_colors_pro,self.selecters_colors_pro)
        self.theme_random=(self.pawn_colors_random,self.grid_colors_random,self.selecters_colors_random)

        self.themes=[self.theme_pro,self.theme_classic,self.theme_random]

    def session(self):
        self.show()
        while self.window.open and not self.board.won:
            self.window.check()
            self.input()
            self.play()
            self.check()
            time.sleep(self.delta)
            self.show()
        self.end()

    def end(self):
        self.board.end()
        self.window.kill()

    def input(self):
        cursor=None
        self.updating=False
        while (not self.updating) and self.window.open:
            self.window.check()
            cursor=self.cursor
            self.click=self.window.click()
            self.cursor=self.board.point(self.window)
            keys=pygame.key.get_pressed()
            if keys[K_RSHIFT] or keys[K_LSHIFT]:
                self.loadThemes()
                self.theme_mode=(self.theme_mode+1)%len(self.themes)
                print(self.theme_mode)
            if cursor==self.cursor and not self.click and not keys[K_RSHIFT] and not keys[K_LSHIFT]:
                self.updating=False
            else:
                self.updating=True

    def play(self):
        click=self.click
        position=self.cursor
        board=self.board #Might add security later even though it's useless
        if board.state%2==0:
            player=self.player1
        else:
            player=self.player2
        player.play(board,position,click)
        if player.hasChosen:
            entity=board.pawn_selecter
            move=board.move_selection
            moves=board.moves_selecter
            if entity is not None and move in moves: #Testing if players choices are possible
                self.board.move(entity,move)
            player.hasChosen=False

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

if __name__=="__main__":
    game=Chess()
