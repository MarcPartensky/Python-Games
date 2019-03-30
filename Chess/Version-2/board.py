from mycolors import *
from pieces import *

from copy import deepcopy
from math import sqrt,atan,cos,sin

import pygame
import random
import time


sign=lambda x:x>=0

class Board:
    def __init__(self):
        self.orientation=1 #Off
        self.flipping=0 #Off
        self.size=(8,8)
        self.state=0
        self.won=False
        self.draw=False
        self.winner=None
        self.historic=[]
        self.grid_historic=[]
        self.action=None
        self.moves_selecter=[]
        self.piece_selecter=None
        self.message=""
        self.promoted=[Queen,Tower,Bishop,Horse]
        self.alphabet="abcdefghijklmnopqrstuvwxyz"
        self.last_action_shown=True
        self.colors=["White","Black"]
        self.time=time.time()
        self.moving_shown=False
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
                p=(x,y)
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

    def __repr__(self):
        sx,sy=self.size
        presentation=""
        for y in range(sy):
            presentation+="|"
            for x in range(sx):
                entity=self.grid[y][x]
                if not entity:
                    presentation+="       "
                else:
                    nature=entity.id
                    nature=nature+str(entity.side)+" "*(6-len(nature))
                    presentation+=nature
                presentation+="|"
            presentation+="\n"
        return presentation


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
        text="|"+str(state)+"| : "+str(self.colors[side-1])+" "+name+" moved in "+spot
        return text


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

    def locateSidePieces(self,side):
        positions=[]
        sx,sy=self.size
        for y in range(sy):
            for x in range(sx):
                entity=self.grid[y][x]
                if entity:
                    if entity.side==side:
                        positions.append((x,y))
        return positions

    def locateAllPieces(self):
        positions=[]
        sx,sy=self.size
        for y in range(sy):
            for x in range(sx):
                entity=self.grid[y][x]
                if entity:
                    positions.append((x,y))
        return positions

    def getSidePieces(self,side):
        pieces=[]
        sx,sy=self.size
        for y in range(sy):
            for x in range(sx):
                entity=self.grid[y][x]
                if entity:
                    if entity.side==side:
                        pieces.append(entity)
        return pieces

    def getAllPieces(self):
        pieces=[]
        sx,sy=self.size
        for y in range(sy):
            for x in range(sx):
                entity=self.grid[y][x]
                if entity:
                    pieces.append(entity)
        return pieces

    def correctMoves(self,moves):
        new_moves=[]
        for move in moves:
            x,y=move
            if self.inGrid(x,y):
                new_moves.append(move)
        return new_moves

    def getSideMoves(self,side,raw=True):
        pieces=self.getSidePieces(side)
        moves=[]
        for piece in pieces:
            moves+=self.getMoves(piece,piece.position,raw)
        return moves

    def removeFromSets(self,set1,set2):
        #Remove all the elements of set1 that are in set2
        new_set=[]
        for e1 in set1:
            if not e1 in set2:
                new_set.append(e1)
        return new_set

    def getSuicideMoves(self,piece,moves):
        enemy_side=self.otherSide(piece.side)
        all_enemy_moves=self.getSideMoves(enemy_side)
        new_moves=[]
        for move in moves:
            if move in all_enemy_moves:
                new_moves.append(move)
        return new_moves

    def oldRemoveSuicideMoves(self,piece,moves):
        #Prevent the king's player from dying on the next turn by removing moves that will get it killed
        enemy_side=self.otherSide(piece.side)
        all_enemy_moves=self.getSideMoves(enemy_side)
        moves=self.removeFromSets(moves,all_enemy_moves)
        return moves

    def removeSuicideMoves(self,dying_piece,choosed_piece,moves):
        new_moves=[]
        #print("In removeSuicideMoves:")
        #print("moves:",moves)
        #print("dying:",dying)
        #print("dying_piece:",dying_piece)
        #print("choosed_piece:",choosed_piece)
        #print("")
        for move in moves:
            dying=self.canDieNextTurn(dying_piece,choosed_piece,move)
            if not dying:
                new_moves.append(move)
        return new_moves

    def canDieNextTurn(self,dying_piece,choosed_piece,choosed_move):
        new_board=deepcopy(self)
        new_board.choose(choosed_piece,choosed_piece.position,choosed_move)
        enemy_side=new_board.otherSide(dying_piece.side)
        all_enemy_moves=new_board.getSideMoves(enemy_side,1)
        #print("In canDieNextTurn:")
        #print("choosed_piece and choosed_move:",choosed_piece,choosed_move)
        #print("dying_piece:",dying_piece)
        #print("enemy_move:",all_enemy_moves)
        #print("new_board:")
        #print(new_board)
        #print("")
        for enemy_move in all_enemy_moves:
            if enemy_move==dying_piece.position:
                return True
        return False



    def otherSide(self,side):
        return side%2+1



    def getMoves(self,piece,position,raw=False):
        #print("In getMoves")
        #print("piece:",piece)
        #print("position:",position)
        moves=self.extractMoves(piece,position)
        #print("normal moves",normal_moves)
        if isinstance(piece,King) or isinstance(piece,Pawn):
            moves+=self.extractSpecialMoves(piece,position)
        #print("special moves",special_moves)
        #print("")
        #moves=normal_moves+special_moves
        #moves=self.correctMoves(moves)
        if not raw: king=self.getById("King",piece.side)
            #moves=self.removeSuicideMoves(king,piece,moves)
        random.shuffle(moves)
        print(moves)
        return moves

    def getRawMoves(self,piece):
        moves=self.extractMoves(piece,piece.position)
        if isinstance(piece,King) or isinstance(piece,Pawn):
            moves+=self.extractSpecialMoves(piece,position)
        random.shuffle(moves)
        return moves

    def extractMoves(self,piece,position):
        vectors,norm=piece.moves
        px,py=position
        sx,sy=self.size
        moves=[]
        orientation=piece.side%2*2-1
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

    def extractSpecialMoves(self,piece,position):
        px,py=position
        sx,sy=self.size
        moves=[]
        if isinstance(piece,Pawn):
            moves+=self.getDiagonalKillMoves(piece)
            moves+=self.getEnPassantMoves(piece)
            moves+=self.getTwoStepsMoves(piece)
        if isinstance(piece,King):
            moves+=self.getRoqueMoves(piece)
        return moves

    def getDiagonalKillMoves(self,piece):
        o=((self.state+1)%2)*2-1
        moves=[]
        px,py=piece.position
        x,y=(px-1,py+o)
        if self.inGrid(x,y):
            entity=self.grid[y][x]
            if entity is not None:
                if entity.side is not piece.side:
                    moves.append((x,y))
        x,y=(px+1,py+o)
        if self.inGrid(x,y):
            entity=self.grid[y][x]
            if entity is not None:
                if entity.side is not piece.side:
                    moves.append((x,y))
        return moves



    def getTwoStepsMoves(self,piece):
        o=((self.state+1)%2)*2-1
        moves=[]
        px,py=piece.position
        if piece.state==0:
            if not self.grid[py+o][px] and not self.grid[py+2*o][px]:
                move=(px,py+2*o)
                moves.append(move)
        return moves


    def getEnPassantMoves(self,piece):
        o=((self.state+1)%2)*2-1
        moves=[]
        px,py=piece.position
        x,y=(px,py+o)
        if len(self.historic)>0:
            piece,position,move=self.historic[-1]
            if isinstance(piece,Pawn):
                ex,ey=position
                emx,emy=move
                x,y=(px-1,py)
                if self.inGrid(x,y):
                    if (x,y)==(emx,emy) and (ex,ey-o)==(emx,emy):
                        moves.append((x,y+o))
                x,y=(px+1,py)
                if self.inGrid(x,y):
                    if (x,y)==(emx,emy) and (ex,ey-o)==(emx,emy):
                        moves.append((x,y+o))
        return moves

    def getRoqueMoves(self,piece):
        o=((self.state+1)%2)*2-1
        moves=[]
        px,py=piece.position
        if piece.state==0 and not piece.check:
            neighbours=self.getNeighbours(piece)
            for neighbour in neighbours:
                if isinstance(neighbour,Tower):
                    if neighbour.state==0:
                        if neighbour.side is piece.side:
                            nx,ny=neighbour.position
                            px,py=piece.position
                            dx=int((nx-px)/abs(nx-px))
                            position=(px+2*dx,py)
                            moves.append(position)
        return moves

    def getTowerMoveFromRoque(self,piece,move):
        px,py=piece.position
        mx,my=move
        if abs(mx-px)!=2:
            return None
        else:
            o=int((mx-px)/(abs(mx-px)))
            print("o:",o)
            tower_move=(px+o,py)
            x=px+o
            while abs(x)<10:
                print("x:",x)
                print("entity:",self.grid[py][x])
                tower=self.grid[py][x]
                if tower:
                    return (tower,tower_move)
                x+=o
            return None





    def getNeighbours(self,piece):
        vectors,norm=piece.moves
        sx,sy=self.size
        m=max(sx,sy)
        norm=m
        px,py=piece.position
        neighbours=[]
        orientation=((self.state+1)%2)*2-1
        for vector in vectors:
            vx,vy=vector
            n=1
            while n<=norm:
                x=px+vx*n
                y=py+orientation*vy*n
                if self.inGrid(x,y):
                    if self.grid[y][x]:
                        entity=self.grid[y][x]
                        if entity.side is piece.side:
                            neighbours.append(entity)
                        break
                else:
                    break
                n=n+1
        return neighbours


    def getById(self,id,side):
        position=self.locateById(id,side)
        if position:
            x,y=position
            entity=self.grid[y][x]
            return entity
        else:
            return None

    def updateCheck(self):
        player_side=(self.state+1)%2+1
        enemy_side=self.state%2+1
        #print("State and sides:",self.state,player_side,enemy_side)
        king=self.getById("King",player_side)
        king.check=self.isInCheck(king)

    def isInCheck(self,king):
        enemy_side=king.side%2+1
        pieces=self.getSidePieces(enemy_side)
        for piece in pieces:
            if king in self.canKill(piece):
                return True
        return False


    def canKill(self,killer):
        moves=self.getMoves(killer,killer.position)
        #print("moves:",moves)
        victims=[]
        for move in moves:
            x,y=move
            #print("canKill move:",move)
            entity=self.grid[y][x]
            if entity:
                victims.append(entity)
        #print("killer:",killer)
        #print("victims:",victims)
        #print("")
        return victims


    def inGrid(self,x,y):
        sx,sy=self.size
        return (0<=x and x<sx and 0<=y and y<sy)

    def move(self,piece,position,move):
        self.choose(piece,position,move)
        self.state+=1
        self.checkPromotion(self.action) #Here "check" means verify
        enemy_side=self.otherSide(piece.side)
        if self.isAlive("King",enemy_side):
            self.updateCheck() #Here "check" is the techical chess term
        #self.state+=1

    def choose(self,piece,position,move):
        mx,my=move
        px,py=position
        self.action=[piece,position,move]
        o=((self.state+1)%2)*2-1
        #print("In choose:")
        #print("piece:",piece)
        #print("position:",position)
        #print("move:",move)
        if not isinstance(piece,Pawn) and not isinstance(piece,King):
            piece.position=move
            self.grid[py][px]=None
            piece.state+=1
            self.grid[my][mx]=piece
        elif isinstance(piece,Pawn):
            #prise en passant
            if mx==px+1 and my==py+o:
                self.grid[py][mx]=None
            if mx==px-1 and my==py+o:
                self.grid[py][mx]=None
            piece.position=move
            self.grid[py][px]=None
            piece.state+=1
            self.grid[my][mx]=piece
        else:
            #The piece is a king
            #print("In choose:")
            #print("piece:",piece)
            if move in self.getRoqueMoves(piece):
                tower,tower_move=self.getTowerMoveFromRoque(piece,move)
                tpx,tpy=tower.position
                tx,ty=tower_move
                tower.position=tower_move
                self.grid[tpy][tpx]=None
                tower.state+=1
                self.grid[ty][tx]=tower
                #print("tower move:")
                #print(tx,ty)
                #print(tpx,tpy)
            print(move,self.getRoqueMoves(piece))
            print("")
            piece.position=move
            self.grid[py][px]=None
            piece.state+=1
            self.grid[my][mx]=piece




    def reverseMove(self):
        if len(self.historic)>1 and len(self.grid_historic)>1:
            self.state-=1
            del self.historic[-1]
            self.action=self.historic[-1]
            del self.grid_historic[-1]
            self.grid=self.grid_historic[-1]
            piece,position,move=self.historic[-1]
            x,y=position
            self.piece_selecter=self.grid[y][x]

    def updateHistoric(self):
        #self.state+=1
        self.historic.append(self.action)
        self.grid_historic.append(deepcopy(self.grid))
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
        orientation=((self.state+1)%2)*2-1
        if isinstance(piece,Pawn):
            if orientation==1 and y==sy-1:
                self.promote(piece,move)
            if orientation==-1 and y==0:
                self.promote(piece,move)

    def promote(self,piece,move):
        x,y=move
        self.grid[y][x]=self.promoted[0](piece.side,move)

    def point(self,window):
        sx,sy=self.size
        wsx,wsy=window.size
        wx,wy=window.point()
        x,y=int(sx*wx/wsx),int(sy*wy/wsy)
        return (x,y)

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
