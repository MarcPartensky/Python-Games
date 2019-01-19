#-------#
#Credits#
#-------#

__author__="Marc Partensky"
__license__="Marc Partensky Company"
__game__="Morpions"

"""This game is available on every computer device that has Python installed."""

#------------#
#Dependencies#
#------------#

import os
os.system("pip2.7 install pygame")
import pygame
from pygame.locals import *
import math
import random
import numpy as np
import time
import copy

try:
    DIRECTORY="/Users/olivierpartensky/Programs/Python/Games/Morpions/"
    os.chdir(DIRECTORY)
finally:
    pass

#---------#
#Variables#
#---------#

BLUE   = (  0,  0,255)
RED    = (255,  0,  0)
GREEN  = (  0,255,  0)
YELLOW = (255,255,  0)
BLACK  = (  0,  0,  0)
WHITE  = (255,255,255)

RIGHT = 0
UP    = 1
LEFT  = 2
DOWN  = 3

#-------#
#Classes#
#-------#

class Window:
    def __init__(self,colors,title=__game__):
        self.color_case,self.color_line=colors
        self.title=title
        self.open=True
        pygame.init()
        info = pygame.display.Info()
        s=max(info.current_w//2,info.current_h//2)
        self.size=(s,s)
        self.screen=pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.title)
        self.font = pygame.font.SysFont("monospace", 65)

    def check(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.open=False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.open=False

    def direction(self):
        keys=pygame.key.get_pressed()
        if keys[K_LEFT]:
            return LEFT
        if keys[K_RIGHT]:
            return RIGHT
        if keys[K_UP]:
            return UP
        if keys[K_DOWN]:
            return DOWN

    def select(self):
        while self.open:
            self.check()
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    return (event.pos[0],event.pos[1])

    def flip(self):
        pygame.display.flip()


    def draw(self,color,coordonnates,size):
        x,y=coordonnates
        sx,sy=size
        pygame.draw.rect(self.screen, color, (x,y,sx,sy), 0)

    def kill(self):
        pygame.quit()

    def pop_up(self,text,colors):
        text_color,background_color,border_color=colors
        sx=len(text)*25
        sy=50
        wx,wy=self.size
        x,y=((wx-sx)/2,(wy-sy)/2)
        p=border_size=1
        pygame.draw.rect(self.screen, border_color, (x,y,sx,sy), 0)
        pygame.draw.rect(self.screen, background_color, (x+p,y+p,sx-2*p,sy-2*p), 0)
        label = self.font.render(text, 1, text_color)
        self.screen.blit(label, (x+2*p,y))

    def pause(self):
        loop=True
        while loop and self.open:
            self.check()
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    loop=False


class Map:
    def __init__(self,players):
        self.size=(3,3) #implementation
        sx,sy=self.size
        self.cases=sx*sy
        self.board=np.zeros(self.size)
        self.player1,self.player2=self.players=players
        self.value1,self.value2=self.values=[1,-1]
        self.empty=0.
        self.state=0
        self.won=False
        self.filled=False

    def play(self,window):
        turn=self.state%2 #extraction
        player=self.players[turn]
        choice=player.play(self,window)
        value=self.values[turn]
        self.add(choice,value)

    def add(self,choice,value):
        x,y=choice
        self.board[y][x]=value #implementation
        self.won=self.checkWin(value)
        self.filled=self.checkFill()
        self.state=self.cases-self.getList(self.board).count(self.empty)

    def checkFill(self):
        board=self.board
        alist=[]
        for column in board:
            alist+=list(column)
        if alist.count(self.empty)==0:
            return True
        else:
            return False

    def checkWin(self,value):
        b=self.board #extraction
        sx,sy=self.size

        if b[0][0]==b[0][1]==b[0][2]==value:
            return True
        if b[1][0]==b[1][1]==b[1][2]==value:
            return True
        if b[2][0]==b[2][1]==b[2][2]==value:
            return True
        if b[0][0]==b[1][0]==b[2][0]==value:
            return True
        if b[0][1]==b[1][1]==b[2][1]==value:
            return True
        if b[0][2]==b[1][2]==b[2][2]==value:
            return True
        if b[0][0]==b[1][1]==b[2][2]==value:
            return True
        if b[0][2]==b[1][1]==b[2][0]==value:
            return True
        return False


    def choices(self):
        sx,sy=self.size
        l=[]
        for y in range(sy):
            for x in range(sx):
                if self.board[y][x]==self.empty:
                    l.append((x,y))
        return l

    def show(self,window):
        window.screen.fill(window.color_line)
        mx,my=self.size #extraction
        wx,wy=window.size
        cx,cy=wx/mx,wy/my
        for x in range(mx): #loop
            for y in range(my):
                window.draw(window.color_case,(x*cx+1,y*cy+1),(cx-1,cy-1))
                if self.board[y][x]==self.value1:
                    self.player1.draw(window,(x*cx,y*cy),(cx,cy))
                if self.board[y][x]==self.value2:
                    self.player2.draw(window,(x*cx,y*cy),(cx,cy))
        window.flip()


    def getList(self,matrix): #addional function
        alist=[]
        for column in matrix:
            alist+=list(column)
        return alist

    def getMatrix(self,list): #addional function
        sq=sqrt(len(list))
        i=0
        matrix=np.zeros((sq,sq))
        for y in range(sq):
            for x in range(sq):
                matrix[y][x]=list[i]
                i+=1
        return matrix


class Player:
    def __init__(self,color,sign):
        self.color=color #implementation
        self.sign=sign

    def draw(self,window,position,size):
        x,y=position #extraction
        sx,sy=size

        if self.sign=="cross":
            pygame.draw.line(window.screen, self.color, (x,y), (x+sx,y+sy), 1)
            pygame.draw.line(window.screen, self.color, (x,y+sy), (x+sx,y), 1)
        if self.sign=="circle":
            position=(x+sx/2,y+sy/2)
            radius=int(min(sx,sy)/2)
            pygame.draw.circle(window.screen, self.color, position, radius, 0)

class Human(Player):
    def __init__(self,color,sign):
        Player.__init__(self,color,sign) #inheritance

    def play(self,map,window):
        turn=map.state%2 #extraction
        value=map.values[turn]
        mx,my=map.size
        wx,wy=window.size

        cx,cy=wx/mx,wy/my#additionnal variables
        selecting=True

        while selecting and window.open: #main loop
            window.check()
            selection=window.select()
            if selection is not None:
                bx,by=selection
                x,y=int(bx/cx),int(by/cy)
                if map.board[y][x]==0:
                    choice=(x,y)
                    return choice



class Robot(Player):
    def __init__(self,color,sign,difficulty=10):
        Player.__init__(self,color,sign) #inheritance
        self.difficulty=difficulty


    def receiveValues(self,map):
        ownTurn=map.state%2 #extraction
        enemyTurn=(map.state+1)%2
        self.ownValue=map.values[ownTurn] #implementation
        self.enemyValue=map.values[enemyTurn]

    def betasimulate(self,map,i):
        choices=map.choices() #extraction
        turn=map.state%2
        value=map.values[turn]
        mx,my=map.size

        coefficient=map.cases-map.state-1 #additionnal variables
        delta=100**coefficient
        gamma=self.canWin(choices,map,value)

        if gamma!=0:
            self.results[i]+=gamma*delta
        else:
            print(gamma)
            for choice in choices: #recursive loop
                new_map=Map(map.players) #map implementation
                new_map.board=copy.deepcopy(map.board)
                new_map.add(choice,value)
            print(new_map.board,new_map.filled)
            if not new_map.filled:
                self.betasimulate(new_map,i) #recursive action

    def canWin(self,choices,map,value):
        for choice in choices: #recursive loop
            new_map=Map(map.players) #map implementation
            new_map.board=copy.deepcopy(map.board)
            new_map.add(choice,value)

            if new_map.checkWin(self.ownValue): #changes
                print(new_map.board)
                print("win, state=",new_map.state)
                return 1
            if new_map.checkWin(self.enemyValue):
                print("loose, state=",new_map.state)
                return -1
        return 0

    def simulate(self,map,i):
        choices=map.choices() #extraction
        turn=map.state%2
        value=map.values[turn]
        mx,my=map.size

        coefficient=map.cases-map.state-1 #additionnal variables
        delta=100**coefficient

        for choice in choices: #recursive loop
            new_map=Map(map.players) #map implementation
            new_map.board=copy.deepcopy(map.board)
            new_map.add(choice,value)
            x,y=choice

            if new_map.checkWin(self.ownValue): #changes
                self.results[i]+=delta
            elif new_map.checkWin(self.enemyValue):
                self.results[i]-=delta
            else:
                if not new_map.filled:
                    self.simulate(new_map,i) #recursive action

    def play(self,map,window):
        self.receiveValues(map) #extraction
        mx,my=map.size
        choices=map.choices()
        sc=len(choices)
        self.results=[0]*sc #additionnal variables

        for i in range(sc): #loop
            choice=choices[i] #extraction
            print("choosing:",choice,i)
            new_map=Map(map.players) #additionnal variables
            new_map.board=copy.deepcopy(map.board)
            new_map.add(choice,self.ownValue)
            self.simulate(new_map,i) #implementation
        choice=self.choose(choices)
        print("choices=",choices)
        print("results=",self.results)
        print("choice=",choice)
        return choice

    def choose(self,choices): #parameters: choices, results and difficulty
        difficulty=self.difficulty #extraction
        results=self.results[:]
        s=len(self.results)
        results.sort() #lists choices from the worst to the best
        v=int((s-1)*difficulty/9) #makes a good or bad choice dependending on difficulty
        r=results[v] #gets a value
        indexes=[] #gets all indexes for a given value
        for i in range(s):
            if r==self.results[i]:
                indexes.append(i)
        index=random.choice(indexes) #randomly chooses an index when values are alike
        return choices[index]


#----------#
#Main class#
#----------#

class Game:
    def __init__(self):
        self.difficulty=9 #from 0 to 9
        self.window_colors=[BLACK,WHITE] #implementation
        self.window=Window(self.window_colors)
        self.player1=Human(BLUE,"cross")
        self.player2=Robot(RED,"circle",self.difficulty)
        self.players=[self.player1,self.player2]
        self.main()

    def main(self):
        while self.window.open: #loop
            self.window.check()
            self.play()

    def play(self):
        self.winner=None
        self.map=Map(self.players)
        self.map.show(self.window)
        while self.window.open and not self.map.won and not self.map.filled: #loop
            self.window.check()
            self.map.play(self.window)
            self.map.show(self.window)
        if self.map.won:
            turn=(self.map.state+1)%2
            self.winner=self.map.players[turn]
        self.dealWithWin()

    def dealWithWin(self):
        winner=self.winner
        if isinstance(winner,Human):
            text="Vous avez gagne."
            text_color=winner.color
        elif isinstance(winner,Robot):
            text="Vous avez perdu."
            text_color=winner.color
        else:
            text="Match nul."
            text_color=WHITE

        colors=(text_color,BLACK,text_color)
        self.window.pop_up(text,colors)
        self.window.flip()
        self.window.pause()






#-------#
#Actions#
#-------#

game=Game()
