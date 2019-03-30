from board import Board

#from random import shuffle


class Player:
    def __init__(self,side):
        self.side=side
        self.alive=True
        self.hasChosen=False
        self.choice=None

    def getAllPieces(self,board):
        pieces=[]
        sx,sy=board.size
        for y in range(sy):
            for x in range(sx):
                position=(x,y)
                entity=board.getEntity(position)
                if entity is not None:
                    pieces.append(entity)
        #shuffle(pieces)
        return pieces

    def getSidePieces(self,board,side):
        pieces=self.getAllPieces(board)
        side_pieces=[]
        for piece in pieces:
            if piece.side is side:
                side_pieces.append(piece)
        return side_pieces

    def getMovablePieces(self,pieces,board):
        movable_pieces=[]
        for piece in pieces:
            position=board.locateByEntity(piece)
            moves=board.getMoves(piece,position)
            ##print(len(moves))
            if len(moves)>0:
                movable_pieces.append(piece)
        return movable_pieces

    def getPossibilities(self,board,side):
        pieces=self.getSidePieces(board,side)
        pieces=self.getMovablePieces(pieces,board)
        output=[]
        for piece in pieces:
            position=board.locateByEntity(piece)
            for move in board.getMoves(piece,position):
                output.append((piece,position,move))
        return output

    def getFastChoices(self,board,side):
        return board.locateChoices(side)

    def analyse(self,board):
        values_counter=0
        sx,sy=board.size
        for y in range(sy):
            for x in range(sx):
                entity=board.grid[y][x]
                if entity:
                    piece=entity
                    if self.side is entity.side:
                        values_counter+=piece.value
                    else:
                        values_counter-=piece.value
        return values_counter
