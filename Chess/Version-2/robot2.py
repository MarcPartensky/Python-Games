from player import Player
from myminimax import Minimax

from copy import deepcopy

class Robot(Player):
    def __init__(self,side,prediction):
        self.id="Robot"
        Player.__init__(self,side)
        self.prediction=prediction
        self.step_choices=1

    def play(self,board,position,click):
        board=self.board
        if board.moving is None or not board.moving_shown:
            self.smartPlay(board.grid)

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

    def smartPlay(self,board).grid:
        tree=self.predict(board,self.prediction)
        minimax=Minimax(tree,0)
        choice=minimax.choice
        possibilities=self.getFastChoices(board,self.side)
        piece,position,move=possibilities[choice]
        board.piece_selecter=piece
        board.moves_selecter=board.getMoves(piece,position)
        board.move_selection=move
        self.choice=board.piece_selecter,move
        self.hasChosen=True

    def predict(self,grid,max_n=1,n=0):
        old_value=self.analyse(grid)
        side=(self.side-1+n)%2+1
        if n<max_n:
            possibilities=self.getFastChoices(board,side)
            ##print(len(possibilities),n)
            storage=[]
            for possibility in possibilities:
                piece,position,move=possibility
                n_board=deepcopy(board)
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
            return self.analyse(grid)

    def analyse(self,grid):
        values_counter=0
        sx,sy=len(grid),len(grid[0])
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
