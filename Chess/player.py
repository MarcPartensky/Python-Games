from myminimax import *

from board import *

import random
import copy

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
        #random.shuffle(pieces)
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

#(1,2)=>(-1/2,1/2)=>(-1,1)

    def analyse(self,board):
        values_counter=0
        sx,sy=board.size
        for y in range(sy):
            for x in range(sx):
                entity=board.grid[y][x]
                if entity is not None:
                    piece=entity
                    if self.side is entity.side:
                        values_counter+=piece.value
                    else:
                        values_counter-=piece.value
        return values_counter


class Robot(Player):
    def __init__(self,side,difficulty=3):
        Player.__init__(self,side)
        self.id="Robot"
        self.difficulty=difficulty
        self.prediction=3
        self.step_choices=1

    def play(self,board,position,click):
        if board.moving is None or not board.moving_shown:
            self.smartPlay(board)

    def randomPlay(self,board):
        pieces=self.getSidePieces(board,self.side)
        pieces=self.getMovablePieces(pieces,board)
        r=random.randint(0,len(pieces)-1)
        piece=pieces[r]
        position=board.locateByEntity(piece)
        moves=board.getMoves(piece,position)
        r=random.randint(0,len(moves)-1)
        move=moves[r]
        board.piece_selecter=piece
        board.moves_selecter=moves
        board.move_selection=move
        self.choice=board.piece_selecter,move
        self.hasChosen=True

    def smartPlay(self,board):
            ##print(len(self.getPossibilities(board,self.side)))
            tree=self.predict(board,self.prediction)
            #print(tree)
            minimax=Minimax(tree,0)
            choice=minimax.choice
            #print(minimax.start)
            #print(choice)
            possibilities=self.getFastChoices(board,self.side)
            piece,position,move=possibilities[choice]
            #print(tree[choice])
            #print(possibilities[choice])
            board.piece_selecter=piece
            board.moves_selecter=board.getMoves(piece,position)
            board.move_selection=move
            self.choice=board.piece_selecter,move
            self.hasChosen=True
            ##print(self.analyse(board))

    def predict(self,board,max_n=1,n=0):
        old_value=self.analyse(board)
        side=(self.side-1+n)%2+1
        ##print("side ",side)
        if n<max_n:
            possibilities=self.getFastChoices(board,side)
            ##print(len(possibilities),n)
            storage=[]
            for possibility in possibilities:
                piece,position,move=possibility
                n_board=copy.deepcopy(board)
                n_board.move(piece,position,move)
                value=self.analyse(board)
                storage.append((n_board,value))
            ##print(storage)
            storage=sorted(storage, key=lambda columns: columns[1],reverse=True)
            ##print(storage)
            storage=storage[:len(storage)-n*self.step_choices]
            #print(storage)
            output=[]
            for n_board,value in storage:
                ##print(value-old_value)
                #if value-old_value>=n*self.step_choices:
                output.append(self.predict(n_board,max_n,n+1))
            return output
        else:
            return self.analyse(board)




class Human(Player):
    def __init__(self,side):
        Player.__init__(self,side)
        self.id="Human"

    def play(self,board,position,click):
        if board.moving is None or not board.moving_shown:
            board.move_selection=position
            if board.piece_selecter is None:
                selection=board.getEntity(position)
                if selection is not None:
                    piece=selection
                    if piece.side is self.side:
                        board.moves_selecter=board.getMoves(piece,position)
                        if click:
                            board.piece_selecter=selection
                            #board.debug()
                else:
                    board.moves_selecter=[]
            else:
                if click:
                    entity=board.getEntity(position)
                    if position in board.moves_selecter:
                        self.hasChosen=True
                        self.choice=board.piece_selecter,position
                    elif entity is not None:
                        if  entity.side is self.side:
                            board.piece_selecter=entity
                            board.moves_selecter=board.getMoves(entity,position)
                        else:
                            board.piece_selecter=None
                            board.moves_selecter=[]
                    else:
                        board.piece_selecter=None
                        board.moves_selecter=[]
