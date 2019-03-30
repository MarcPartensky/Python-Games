import pygame

class Pawn:
    def __init__(self,side,color,position):
        self.side=side
        self.color=color
        self.position=position
        self.diagonal1=[(i,i) for i in range(-10,10)]
        self.diagonal2=[(-i,i) for i in range(-10,10)]
        self.horizontal=[(i,0) for i in range(-10,10)]
        self.vertical=[(0,i) for i in range(-10,10)]
        self.moves=[]
        self.special_moves=[]
        self.steps=0

    def getMoves(self,board):
        moves=[]
        for move in self.moves:
            x,y=move
            entity=board.grid[y][x]
            if entity is None:
                moves.append(move)
            else:
                if entity.side!=self.side:
                    moves.append(move)

        for move in special_moves:
            x,y,condition=move
            if condition(board):
                entity=board.grid[y][x]
                if entity is None:
                    moves.append(move)
                else:
                    if entity.side!=self.side:
                        moves.append(move)


    def showMoves(self,moves,board,window):
        wsx,wsy=window.size
        sx,sy=board.size
        for move in moves:
            x,y=move
            raw_position=[x*wsx/sx,y*wsy/sy]
            raw_radius=min(wsx/sx,wsy/sy)*2/3
            pygame.draw.circle(window.screen,board.potential_moves_color,raw_position,raw_radius,0)



    def show(self,coordonnates,window):
        x,y,sx,sy=coordonnates
        picture=pygame.image.load(self.picture_directory)
        picture=pygame.transform.scale(picture,(sx,sy))
        picture=colorize(picture,self.color)
        window.screen.blit(picture, (x,y))

class Knight(Pawn):
    def __init__(self,side,color,position):
        Pawn.__init__(self,side,color,position)
        self.moves=[(0,1)]
        self.special_moves=[(0,2,self.twoSteps)]
        #prise en passant a ajouter
        self.picture_directory="Pictures/knight.png"

    def twoSteps(self,board):
        return self.steps==0


class Tower(Pawn):
    def __init__(self,side,color,position):
        Pawn.__init__(self,side,color,position)
        self.moves=self.horizontal+self.vertical
        self.picture_directory="Pictures/tower.png"

class Bishop(Pawn):
    def __init__(self,side,color,position):
        Pawn.__init__(self,side,color,position)
        self.moves=self.diagonal1+self.diagonal2
        self.picture_directory="Pictures/bishop.png"

class Horse(Pawn):
    def __init__(self,side,color,position):
        Pawn.__init__(self,side,color,position)
        self.moves=[(-2, 1), ( 2, 1),
                    (-2,-1), ( 2,-1)]
        self.picture_directory="Pictures/horse.png"

class Queen(Pawn):
    def __init__(self,side,color,position):
        Pawn.__init__(self,side,color,position)
        self.moves=self.horizontal+self.vertical+self.diagonal1+self.diagonal2
        self.picture_directory="Pictures/queen.png"

class King(Pawn):
    def __init__(self,side,color,position):
        Pawn.__init__(self,side,color,position)
        self.moves=[(-1, 1), ( 0, 1), ( 1, 1),
                    (-1, 0), ( 0, 0), ( 1, 0),
                    (-1,-1), ( 0,-1), ( 1,-1)]
        #roc a ajouter
        self.picture_directory="Pictures/king.png"

def colorize(image, newColor):
    image = image.copy()
    image.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
    image.fill(newColor[0:3] + (0,), None, pygame.BLEND_RGBA_ADD)
    return image
