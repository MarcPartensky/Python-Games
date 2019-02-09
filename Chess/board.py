from mycolors import *
from pieces import *

import pygame
import random
import time
import math
from math import sqrt,atan,cos,sin


def sign(number):
    if number>=0:
        return 1
    else:
        return -1

class Board:
    def __init__(self):
        self.orientation=1 #Off
        self.flipping=0 #Off
        self.size=(8,8)
        self.state=0
        self.won=False
        self.winner=None
        self.historic=[]
        self.action=None
        self.moves_selecter=[]
        self.piece_selecter=None
        self.message=""
        self.promoted=[Queen,Tower,Bishop,Horse]
        self.alphabet="abcdefghijklmnopqrstuvwxyz"
        self.last_action_shown=True
        self.colors=["White","Black"]
        self.time=time.time()
        self.moving_shown=True
        self.moving=None
        self.moving_time=0
        self.moving_max_time=2
        self.moving_position=None
        self.wait=False
        self.generate()

    def generate(self):
        self.grid= [["t1","h1","b1","g1","q1","b1","h1","t1"],
                    ["k1","k1","k1","k1","k1","k1","k1","k1"],
                    ["nn","nn","nn","nn","nn","nn","nn","nn"],
                    ["nn","nn","nn","nn","nn","nn","nn","nn"],
                    ["nn","nn","nn","nn","nn","nn","nn","nn"],
                    ["nn","nn","nn","nn","nn","nn","nn","nn"],
                    ["k2","k2","k2","k2","k2","k2","k2","k2"],
                    ["t2","h2","b2","g2","q2","b2","h2","t2"]]
        sx,sy=self.size
        for y in range(sy):
            for x in range(sx):
                p=[x,y]
                small_id=self.grid[y][x]
                if small_id=="k1":
                    entity=Pawn(1,p)
                elif small_id=="k2":
                    entity=Pawn(2,p)
                elif small_id=="h1":
                    entity=Horse(1,p)
                elif small_id=="h2":
                    entity=Horse(2,p)
                elif small_id=="b1":
                    entity=Bishop(1,p)
                elif small_id=="b2":
                    entity=Bishop(2,p)
                elif small_id=="b1":
                    entity=Bishop(1,p)
                elif small_id=="b2":
                    entity=Bishop(2,p)
                elif small_id=="t1":
                    entity=Tower(1,p)
                elif small_id=="t2":
                    entity=Tower(2,p)
                elif small_id=="g1":
                    entity=King(1,p)
                elif small_id=="g2":
                    entity=King(2,p)
                elif small_id=="q1":
                    entity=Queen(1,p)
                elif small_id=="q2":
                    entity=Queen(2,p)
                else:
                    entity=None
                self.grid[y][x]=entity

    def debug(self):
        pass
        #print("DEBUG:")
        #print(self.state)
        #print(self.piece_selecter)
        #print(self.moves_selecter)
        #print("")

    def getPresentation(self,state,action):
        sx,sy=self.size
        piece,position,move=action
        name=piece.name
        side=piece.side
        x,y=move
        spot=self.alphabet[x%sx]+str(sy-y)
        return "|"+str(state)+"| : "+str(self.colors[side-1])+" "+name+" moved in "+spot


    def summarize(self,historic):
        for state in range(len(historic)):
            action=historic[state]
            self.message+=self.getPresentation(state,action)

    def isAlive(self,id,side):
        if self.locateById(id,side) is not None:
            return True
        else:
            return False

    def locateChoices(self,side):
        ##print(side)
        output=[]
        sx,sy=self.size
        for y in range(sy):
            for x in range(sx):
                entity=self.grid[y][x]
                if entity is None:
                    continue
                if entity.side!=side:
                    continue
                moves=self.getMoves(entity,(x,y))
                if len(moves)==0:
                    continue
                for move in moves:
                    output.append((entity,(x,y),move))
        #print(output)
        return output




    def locateById(self,id,side):
        sx,sy=self.size
        for y in range(sy):
            for x in range(sx):
                entity=self.grid[y][x]
                if entity is not None:
                    if entity.side is side and entity.id is id:
                        return (x,y)
        return None

    def locateByEntity(self,piece):
        sx,sy=self.size
        for y in range(sy):
            for x in range(sx):
                if self.grid[y][x] is piece:
                    return (x,y)
        return None

    def getMoves(self,piece,position):
        moves=self.extractMoves(piece,position)
        moves+=self.extractSpecialMoves1(piece,position)
        ##print(moves)
        random.shuffle(moves)
        ##print(moves)
        ##print("")
        return moves

    def extractMoves(self,piece,position):
        vectors,norm=piece.moves
        px,py=position
        sx,sy=self.size
        moves=[]
        orientation=((self.state+1)%2)*2-1
        for vector in vectors:
            vx,vy=vector
            n=1
            while n<=norm:
                x=px+vx*n
                y=py+orientation*vy*n
                if 0<=x and x<sx and 0<=y and y<sy:
                    if self.grid[y][x] is None:
                        moves.append((x,y))
                    else:
                        entity=self.grid[y][x]
                        if (entity.side is not piece.side) and piece.direct_kill:
                            moves.append((x,y))
                        break
                n=n+1
        return moves

    def extractSpecialMoves1(self,piece,position):
        px,py=position
        o=orientation=((self.state+1)%2)*2-1
        moves=[]
        if isinstance(piece,Pawn):
            x,y=(px+1,py+o)
            if self.inGrid(x,y):
                entity=self.grid[y][x]
                if entity is not None:
                    if entity.side is not piece.side:
                        moves.append((x,y))
            x,y=(px-1,py+o)
            if self.inGrid(x,y):
                entity=self.grid[y][x]
                if entity is not None:
                    if entity.side is not piece.side:
                        moves.append((x,y))
        ##print(moves)
        return moves

    def inGrid(self,x,y):
        sx,sy=self.size
        return (0<=x and x<sx and 0<=y and y<sy)

    def move(self,piece,position,move):
        mx,my=move
        px,py=position
        self.grid[py][px]=None
        self.grid[my][mx]=piece
        self.action=[piece,position,move]

    def reverseMove(self):
        if self.state>1:
            self.grid[y][x]=None
            del self.historic[-1]
            self.state-=1
            self.action=self.historic[-1]
            self.piece_selecter,position,move=self.historic[-1]

    def updateHistoric(self):
        self.state+=1
        self.historic.append(self.action)
        self.piece_selecter=None
        self.moves_selecter=[]
        self.moving=self.action[0]
        self.moving_time=0
        self.time=time.time()


    def check(self):
        sx,sy=self.size
        player1_alive=self.isAlive(King,1)
        player2_alive=self.isAlive(King,2)
        if player1_alive and player2_alive:
            self.won=False
        else:
            self.won=True

    def checkPromotion(self,action):
        sx,sy=self.size
        piece,position,move=action
        x,y=move
        o=orientation=((self.state+1)%2)*2-1
        if isinstance(piece,Pawn):
            if orientation==1 and y==sy-1:
                self.promote(piece,move)
            if orientation==-1 and y==0:
                self.promote(piece,move)

    def promote(self,piece,move):
        x,y=move
        self.grid[y][x]=self.promoted[0]

    def point(self,window):
        sx,sy=self.size
        wsx,wsy=window.size
        wx,wy=window.point()
        x,y=int(sx*wx/wsx),int(sy*wy/wsy)
        return x,y

    def getEntity(self,position):
        sx,sy=self.size
        x,y=position
        if 0<=x and x<sx and 0<=y and y<sy:
            return self.grid[y][x]
        else:
            return None

    def getShownItems(self,grid,moves):
        sx,sy=self.size
        shown_grid=[[None for x in range(sx)] for y in range(sy)]
        moves=[None for i in range(len(self.moves_selecter))]
        if self.orientation:
            for y in range(sy):
                for x in range(sx):
                    shown_grid[x][y]=self.grid[y][x]
            for i in range(len(self.moves_selecter)):
                x,y=self.moves_selecter[i]
                moves=[(y,x)]
        if self.flipping and self.state%2==1:
            for y in range(sy):
                for x in range(sx):
                    shown_grid[sy-1-y][sx-1-x]=self.grid[y][x]
            for i in range(len(self.moves_selecter)):
                x,y=self.moves_selecter[i]
                moves=[(sy-1-y,sx-1-x)]
        return (shown_grid,moves)

    def show(self,window,colors):
        self.pieces_colors,self.grid_colors,self.selecters_colors=colors
        self.case_colors,self.line_color=self.grid_colors
        self.piece_selecter_colors,self.moves_selecter_colors,self.last_piece_selecter_colors,self.last_move_selecter_colors=self.selecters_colors
        #grid,moves=self.getShownItems(self.grid,self.moves_selecter)
        grid,moves=self.grid,self.moves_selecter
        self.showGrid(window)
        if self.state>0 and self.last_action_shown:
            self.showLastPieceSelecter(window)
            self.showLastMoveSelecter(window)
        if self.piece_selecter is not None:
            self.showPieceSelecter(window)
        if self.moves_selecter!=[]:
            self.showMovesSelecter(window)
        self.showPieces(grid,window)
        if self.moving_shown and self.moving is not None and self.moving_position is not None:
            ##print(self.moving_shown,self.moving,self.moving_position)
            self.showMovingPiece(window)
            window.flip()

    def showGrid(self,window):
        i=1
        wsx,wsy=window.size
        sx,sy=self.size
        for y in range(sy):
            i=(i+1)%len(self.case_colors)
            for x in range(sx):
                i=(i+1)%len(self.case_colors)
                coordonnates=[float(x*wsx)/sx,float(y*wsy)/sy,float(wsx)/sx+1,float(wsy)/sy+1]
                pygame.draw.rect(window.screen,self.case_colors[i],coordonnates,0)
        for x in range(sx+1):
            start= (float(x*wsx)/sx,0)
            end=   (float(x*wsx)/sx,wsx)
            pygame.draw.line(window.screen,self.line_color,start,end,1)
        for y in range(sy+1):
            start= (0,float(y*wsy)/sy)
            end=   (wsy,float(y*wsy)/sy)
            pygame.draw.line(window.screen,self.line_color,start,end,1)


    def showPieces(self,grid,window):
        wsx,wsy=window.size
        sx,sy=self.size
        for y in range(sy):
            for x in range(sx):
                entity=grid[y][x]
                if entity is not None:
                    if entity is not self.moving or not self.moving_shown:
                        position=[x*wsx/sx,y*wsy/sy]
                        size=[wsx/sx,wsy/sy]
                        coordonnates=position+size
                        entity.show(window,coordonnates,self.pieces_colors)

    def showMovingPiece(self,window):
        x,y=self.moving_position
        wsx,wsy=window.size
        sx,sy=self.size
        ##print(x,y)
        position=[int(x*wsx/sx),(y*wsy/sy)]
        size=[wsx/sx,wsy/sy]
        coordonnates=position+size
        self.moving.show(window,coordonnates,self.pieces_colors)

    def showMovesSelecter(self,window):
        moves=self.moves_selecter
        wsx,wsy=window.size
        sx,sy=self.size
        sm=min(sx,sy)
        wsm=min(wsx,wsy)
        raw_radius=int(wsm/(sm*4))
        for move in moves:
            x,y=move
            raw_position=(int(wsx*(x+0.5)/sx),int(wsy*(y+0.5)/sy))
            pygame.draw.circle(window.screen, self.moves_selecter_colors[1], raw_position, raw_radius+2, 0)
            pygame.draw.circle(window.screen, self.moves_selecter_colors[0], raw_position, raw_radius, 0)

    def showLastMoveSelecter(self,window):
        pawn,position,move=self.historic[-1]
        wsx,wsy=window.size
        sx,sy=self.size
        sm=min(sx,sy)
        wsm=min(wsx,wsy)
        raw_radius=int(wsm/(sm*4))
        x,y=position
        raw_position=(int(wsx*(x+0.5)/sx),int(wsy*(y+0.5)/sy))
        pygame.draw.circle(window.screen, self.last_move_selecter_colors[1], raw_position, raw_radius+2, 0)
        pygame.draw.circle(window.screen, self.last_move_selecter_colors[0], raw_position, raw_radius, 0)

    def showPieceSelecter(self,window):
        x,y=self.locateByEntity(self.piece_selecter)
        wsx,wsy=window.size
        sx,sy=self.size
        sm=min(sx,sy)
        wsm=min(wsx,wsy)
        raw_radius=int(wsm/(sm*3))
        raw_position=(int(wsx*(x+0.5)/sx),int(wsy*(y+0.5)/sy))
        pygame.draw.circle(window.screen, self.piece_selecter_colors[1], raw_position, raw_radius+2, 0)
        pygame.draw.circle(window.screen, self.piece_selecter_colors[0], raw_position, raw_radius, 0)

    def showLastPieceSelecter(self,window):
        pawn,position,move=self.historic[-1]
        self.time
        x,y=move
        wsx,wsy=window.size
        sx,sy=self.size
        sm=min(sx,sy)
        wsm=min(wsx,wsy)
        raw_radius=int(wsm/(sm*3))
        raw_position=(int(wsx*(x+0.5)/sx),int(wsy*(y+0.5)/sy))
        pygame.draw.circle(window.screen, self.last_piece_selecter_colors[1], raw_position, raw_radius+2, 0)
        pygame.draw.circle(window.screen, self.last_piece_selecter_colors[0], raw_position, raw_radius, 0)

    def getOldTrajectory(self,A,B,moving_time,moving_max_time):
        xa,ya=A
        xb,yb=B
        height=yb-ya
        width=xb-xa
        angle=atan(height/width)
        delta=moving_max_time
        c=moving_time/moving_max_time
        ##print(1-c**2,c,moving_time,moving_max_time)
        z=sqrt((1-c**2))
        x=width*z*cos(angle)
        y=height*z*sin(angle)
        return (x,y)

    def getTrajectory(self):
        piece,old_position,new_position=self.historic[-1]
        xa,ya=old_position
        xb,yb=new_position
        height=yb-ya
        width=xb-xa
        t=self.moving_time
        mt=self.moving_max_time
        ##print("time: ",t,mt)
        x=xa+width*t/mt
        y=ya+height*t/mt
        ##print("trajectory:",x,y)
        return (x,y)

    def updateMoving(self,window,colors):
        piece,old_position,new_position=self.historic[-1]
        dt=time.time()-self.time
        self.moving_time=dt
        ox,oy=old_position
        nx,ny=new_position
        x,y=self.getTrajectory()
        if min(ox,nx)<=x and x<=max(ox,nx) and min(oy,ny)<=y and y<=max(oy,ny) and self.moving_time<self.moving_max_time:
            self.moving_position=(x,y)
            self.show(window,colors)
        else:
            self.moving_position=(nx,ny)
            self.show(window,colors)
            self.moving=None
            self.moving_position=None
            self.moving_time=0


    def end(self):
        #self.summarize(self.historic)
        self.message+="\n\n"
        self.message+="|=====================|\n"
        if self.won is True:
            self.message+="|   Congratulations   |\n|Player"+str(self.winner.side)+" won the game.|\n"
        else:
            self.message+="|         Tie         |\n"
        self.message+="|=====================|\n"
        #print(self.message)
