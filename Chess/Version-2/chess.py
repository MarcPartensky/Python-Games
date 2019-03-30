from mywindow import *
from mycolors import *

from pieces import King
from board import Board
from player import Player
from human import Human
from robot import Robot

from copy import deepcopy

import json
import time
import pygame
from pygame.locals import *
import os

class Chess:
    def __init__(self,window,players=[Human(1),Human(2)],theme_mode=0):
        self.name="Chess"
        self.theme_mode=theme_mode
        self.loadThemes()
        self.window=window
        self.window.name=self.name
        if not self.window.built:
            self.window.build()
        self.players=players
        self.board=Board()
        self.cursor=None
        self.click=None

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
            turn=self.board.state%2
            player=self.players[turn]
            if isinstance(player,Human):
                self.input()
            else:
                if self.board.moving_shown and self.board.moving is not None:
                    self.board.updateMoving(self.window,self.theme)
            self.play()
            self.check()
            self.show()
        self.finalScene()

    def finalScene(self):
        wsx,wsy=window.size
        position=[wsx//6,4*wsy//9]
        size=[3*wsx//4,wsy//10]
        color=WHITE
        self.window.draw.rect(self.window.screen,color,position+size,0)
        color=BLACK
        position=[position[0]+2,position[1]+2]
        size=[size[0]-4,size[1]-4]
        self.window.draw.rect(self.window.screen,color,position+size,0)
        if self.board.draw:
            self.window.alert("Draw")
        else:
            if self.board.won:
                self.window.alert("The winner is Player"+str(self.board.winner.side))
            else:
                self.window.alert("No winner")
        self.window()




    def end(self):
        self.board.end()
        self.window.kill()

    def input(self):
        cursor=None
        self.updating=False
        while (not self.updating) and self.window.open:
            self.window.check()
            typing=False
            if self.board.moving_shown and self.board.moving is not None:
                self.board.updateMoving(self.window,self.theme)
            cursor=self.cursor
            self.click=self.window.click()
            self.cursor=self.board.point(self.window)
            keys=pygame.key.get_pressed()
            if keys[K_LEFT] or keys[K_DOWN]:
                self.board.reverseMove()
                typing=True
            if keys[K_RSHIFT] or keys[K_SPACE]:
                self.loadThemes()
                l=len(self.themes)
                self.theme_mode=(self.theme_mode+l-1)%l
                typing=True
            if keys[K_LSHIFT]:
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
        turn=self.board.state%2
        if len(self.board.getSideMoves(self.players[turn].side))==0:
            self.board.draw=True #Match Nul
            self.updating=False
        else:
            board=self.board #supposed to be giving the player a copy of the board, but is actually giving the actual one
            self.players[turn].play(board,position,click)
            if self.players[turn].hasChosen:
                entity=board.piece_selecter
                move=board.move_selection
                position=board.locateByEntity(entity)
                moves=board.getMoves(entity,position)
                if entity and move in moves: #Testing if player's choice is possible before changing the true board
                    self.board.move(entity,position,move)
                    self.board.updateHistoric()
                    print(self.board.getPresentation(board.state,(entity,position,move)))
                self.players[turn].hasChosen=False

    def check(self):
        self.players[0].alive=self.board.isAlive("King",1)
        self.players[1].alive=self.board.isAlive("King",2)
        if self.players[0].alive and self.players[1].alive:
            self.board.won=False
        else:
            self.board.won=True
            if self.players[0].alive:
                self.board.winner=self.players[0]
            if self.players[1].alive:
                self.board.winner=self.players[1]

    def show(self):
        self.theme=self.themes[self.theme_mode]
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
    #print(directory)
    #print("\n\n")
    human=Human(1)
    robot=Robot(2,prediction=3)
    players=[human,robot]
    window=Window(build=False,size=[700,700])
    game=Chess(window,players)
    game()
    #game.save()
    game.end()
