from player import Player

class Human(Player):
    def __init__(self,side):
        self.id="Human"
        Player.__init__(self,side)

    def play(self,board,position,click):
            #To completed yet
        if not board.moving or not board.moving_shown:
            board.move_selection=position
            if not board.piece_selecter:
                selection=board.getEntity(position)
                if selection:
                    piece=selection
                    if piece.side is self.side:
                        board.moves_selecter=board.getMoves(piece,position)
                        if click:
                            board.piece_selecter=selection
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
