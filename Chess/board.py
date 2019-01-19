from mycolors import *
from pawns import *
import pygame

class Board:
    def __init__(self):
        self.vertical_flip=1 #Off
        self.horizontal_flip=1 #Off
        self.vertical_fliping=0 #Off
        self.horizontal_fliping=0 #Off
        self.size=(8,8)
        self.state=0
        self.won=False
        self.winner=None
        self.historic=[]
        self.moves_selecter=[]
        self.pawn_selecter=None
        self.message=""
        self.promoted=[Horse,Bishop,Tower,Queen]
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
                    entity=Knight(1,p)
                elif small_id=="k2":
                    entity=Knight(2,p)
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
        print(board.state)
        print(board.pawn_selecter)
        print(board.moves_selecter)
        print("")

    def isAlive(self,id,side):
        if self.locateById(id,side) is not None:
            return True
        else:
            return False

    def locateById(self,id,side):
        sx,sy=self.size
        for y in range(sy):
            for x in range(sx):
                entity=self.grid[y][x]
                if entity is not None:
                    if entity.side is side and entity.id is id:
                        return (x,y)
        return None

    def locateByEntity(self,pawn):
        sx,sy=self.size
        for y in range(sy):
            for x in range(sx):
                if self.grid[y][x] is pawn:
                    return (x,y)
        return None

    def getMoves(self,pawn,position):
        moves=self.extractMoves(pawn,position)
        #moves+=self.extractSpecialMoves(pawn,position)
        return moves

    def extractMoves(self,pawn,position):
        vectors,norm=pawn.moves
        px,py=position
        sx,sy=self.size
        moves=[]
        orientation=((self.state+1)%2)*2-1
        print(orientation)
        for vector in vectors:
            vx,vy=vector
            n=1
            while n<=norm:
                x=px+orientation*vx*n
                y=py+orientation*vy*n
                if 0<=x and x<sx and 0<=y and y<sy:
                    if self.grid[y][x] is None:
                        moves.append((x,y))
                    else:
                        entity=self.grid[y][x]
                        if entity.side is not pawn.side and entity.direct_kill:
                            moves.append((x,y))
                        break
                n=n+1
        return moves

    def extractSpecialMoves(pawn,position):
        return moves

    def move(self,pawn,move):
        print("enterin the move function")
        nx,ny=move
        ox,oy=self.locateByEntity(pawn)
        self.grid[oy][ox]=None
        self.grid[ny][nx]=pawn
        self.state+=1
        self.historic.append([pawn,move])
        self.pawn_selecter=None
        self.moves_selecter=[]


    def check(self):
        sx,sy=self.size
        player1_alive=self.isAlive(King,1)
        player2_alive=self.isAlive(King,2)
        if player1_alive and player2_alive:
            self.won=False
        else:
            self.won=True


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

    def show(self,window,colors):
        self.pawns_colors,self.grid_colors,self.selecters_colors=colors
        self.case_colors,self.line_color=self.grid_colors
        self.pawn_selecter_colors,self.moves_selecter_colors=self.selecters_colors
        self.showGrid(window)
        if self.pawn_selecter is not None:
            self.showPawnSelecter(window)
        if self.moves_selecter!=[]:
            self.showMovesSelecter(window)
        self.showPawns(window)

    def showGrid(self,window):
        i=1
        wsx,wsy=window.size
        sx,sy=self.size
        for y in range(sy):
            i=(i+1)%2
            for x in range(sx):
                i=(i+1)%2
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


    def showPawns(self,window):
        wsx,wsy=window.size
        sx,sy=self.size
        for y in range(sy):
            for x in range(sx):
                entity=self.grid[y][x]
                if entity is not None:
                    position=[x*wsx/sx,y*wsy/sy]
                    size=[wsx/sx,wsy/sy]
                    coordonnates=position+size
                    entity.show(window,coordonnates,self.pawns_colors)

    def showMovesSelecter(self,window):
        moves=self.moves_selecter
        wsx,wsy=window.size
        sx,sy=self.size
        sm=min(sx,sy)
        wsm=min(wsx,wsy)
        raw_radius=wsm/(sm*4)
        for move in moves:
            x,y=move
            raw_position=(int(wsx*(x+0.5)/sx),int(wsy*(y+0.5)/sy))
            pygame.draw.circle(window.screen, self.moves_selecter_colors[1], raw_position, raw_radius+2, 0)
            pygame.draw.circle(window.screen, self.moves_selecter_colors[0], raw_position, raw_radius, 0)

    def showPawnSelecter(self,window):
        x,y=self.locateByEntity(self.pawn_selecter)
        wsx,wsy=window.size
        sx,sy=self.size
        sm=min(sx,sy)
        wsm=min(wsx,wsy)
        raw_radius=wsm/(sm*3)
        raw_position=(int(wsx*(x+0.5)/sx),int(wsy*(y+0.5)/sy))
        pygame.draw.circle(window.screen, self.pawn_selecter_colors[1], raw_position, raw_radius+2, 0)
        pygame.draw.circle(window.screen, self.pawn_selecter_colors[0], raw_position, raw_radius, 0)

    def end(self):
        self.message+="|=====================|\n"
        if self.won is True:
            self.message+="|Congratulations!     |\n|Player"+str(self.winner.side)+" won the game.|\n"
        else:
            self.message+="|Tie                  |\n"
        self.message+="|=====================|\n"
        print(self.message)
