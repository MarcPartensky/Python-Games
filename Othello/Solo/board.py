from mycolors import *

import pygame

class Board:
    def __init__(self,theme,size=[8,8]):
        self.size=size
        self.createGrid()
        self.grid_color,self.pieces_color,self.moves_color=theme
        self.moves=[]
        self.won=False


    def createGrid(self):
        sx,sy=self.size
        self.grid=[[0 for x in range(sx)] for y in range(sy)]
        self.grid[3][3]=1
        self.grid[4][3]=2
        self.grid[3][4]=2
        self.grid[4][4]=1

    def inGrid(self,position):
        sx,sy=self.size
        x,y=position
        return (0<=x<sx and 0<=y<sy)


    def adjust(self,raw_position,window):
        wsx,wsy=window.size
        sx,sy=self.size
        rx,ry=raw_position
        return (int(rx*sx/wsx),int(ry*sy/wsy))

    def check(self):
        counter=0
        for column in self.grid:
            counter+=column.count(0)
        print(counter)
        if counter==0:
            self.won=True

    def getMoves(self,player_side,window):
        print(player_side)
        enemy_side=(player_side+1)%2
        positions=self.getPieces(enemy_side)
        for position in positions:
            self.debugMove(position,window,PURPLE)
        positions=self.getAround(positions)
        for position in positions:
            self.debugMove(position,window,YELLOW)

        moves=[]
        for position in positions:
            if self.possibleMove(position,player_side,window):
                moves.append(position)
        return moves

    def getPieces(self,side):
        positions=[]
        print(side)
        side+=1
        sx,sy=self.size
        for y in range(sy):
            for x in range(sx):
                case=self.grid[y][x]
                if case==side:
                    positions.append((x,y))
        return positions

    def getAround(self,positions):
        environment=[]
        around=[(x,y) for x in range(-1,2) for y in range(-1,2) if (x,y)!=(0,0)]
        for position in positions:
            px,py=position
            for step in around:
                stx,sty=step
                x,y=(px+stx,py+sty)
                if self.inGrid((x,y)):
                    if self.grid[y][x]==0:
                        environment.append((x,y))
        return environment

    def conquer(self,position,p_side):
        px,py=position
        p_side+=1
        e_side=p_side%2+1
        sx,sy=self.size
        around=[(x,y) for x in range(-1,2) for y in range(-1,2) if (x,y)!=(0,0)]
        found=False
        for i in range(8):
            norm=0
            vx,vy=around[i] #get vector
            found=False
            possible=False
            eatables=[]
            while not found:
                norm+=1
                x,y=(px+vx*norm,py+vy*norm)
                if self.inGrid((x,y)):
                    case=self.grid[y][x]
                    if case==0:
                        break
                    if case==e_side:
                        possible=True
                        eatables.append((x,y))
                    if case==p_side and norm>1 and possible:
                        found=True
                        for eatable in eatables:
                            x,y=eatable
                            self.grid[y][x]=p_side
                else:
                    break


            i+=1
        return found


    def possibleMove(self,position,p_side,window):
        self.debugMove(position,window,YELLOW)
        px,py=position
        p_side+=1
        e_side=p_side%2+1
        sx,sy=self.size
        around=[(x,y) for x in range(-1,2) for y in range(-1,2) if (x,y)!=(0,0)]
        found=False
        i=0
        while not found and i<len(around):
            norm=0
            vx,vy=around[i] #get vector
            found=False
            possible=False
            while not found:
                norm+=1
                x,y=(px+vx*norm,py+vy*norm)
                if self.inGrid((x,y)):
                    print((x,y))
                    self.debugMove(position,window,BLUE)
                    case=self.grid[y][x]
                    if case==0:
                        break
                    if case==e_side:
                        possible=True
                    if case==p_side and norm>1 and possible:
                        found=True
                else:
                    break
            i+=1
        print("")
        return found

    def show(self,window):
        self.showGrid(window)
        self.showPieces(window)
        self.showMoves(window)

    def debugMove(self,position,window,color):
        #window.clear()
        #self.show(window)
        #self.showMove(position,window,color)
        #window.flip()
        #window.pause()
        pass

    def showMove(self,move,window,color):
        wsx,wsy=window.size
        sx,sy=self.size
        radius=int(min(wsx,wsy)/min(sx,sy)/4)
        x,y=move
        raw_position=(int((x+1/2)*wsx/sx),int((y+1/2)*wsy/sy))
        pygame.draw.circle(window.screen,color,raw_position,radius,0)

    def showMoves(self,window):
        for move in self.moves:
            self.showMove(move,window,self.moves_color)



    def showGrid(self,window):
        wsx,wsy=window.size
        sx,sy=self.size
        for y in range(sy):
            _y=y*wsy//sy
            start=(0,_y)
            end=(wsx,_y)
            pygame.draw.line(window.screen,self.grid_color,start,end,1)
        for x in range(sx):
            _x=x*wsx//sx
            start=(_x,0)
            end=(_x,wsy)
            pygame.draw.line(window.screen,self.grid_color,start,end,1)

    def showPieces(self,window):
        wsx,wsy=window.size
        sx,sy=self.size
        radius=int(min(wsx,wsy)/min(sx,sy)/2)
        for y in range(sy):
            for x in range(sx):
                case=self.grid[y][x]
                raw_position=(int((x+1/2)*wsx/sx),int((y+1/2)*wsy/sy))
                if case==1:
                    color=self.pieces_color[0]
                    pygame.draw.circle(window.screen,color,raw_position,radius,0)
                if case==2:
                    color=self.pieces_color[1]
                    pygame.draw.circle(window.screen,color,raw_position,radius,0)
