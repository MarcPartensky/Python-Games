class Player:
    def __init__(self,side):
        self.side=side
        self.alive=True
        self.hasChosen=False
        self.choice=None


class Robot(Player):
    def __init__(self,side,difficulty=3):
        Player.__init__(self,side)
        self.id="Robot"
        self.difficulty=difficulty

    def play(self,board,position,click):
        pass

class Human(Player):
    def __init__(self,side):
        Player.__init__(self,side)
        self.id="Human"

    def play(self,board,position,click):
        board.move_selection=position
        if board.pawn_selecter is None:
            selection=board.getEntity(position)
            if selection is not None:
                pawn=selection
                if pawn.side is self.side:
                    board.moves_selecter=board.getMoves(pawn,position)
                    if click:
                        board.pawn_selecter=selection
            else:
                board.moves_selecter=[]
        else:
            if click:
                entity=board.getEntity(position)
                if position in board.moves_selecter:
                    self.hasChosen=True
                    self.choice=board.pawn_selecter,position
                elif entity is not None:
                    if  entity.side is self.side:
                        board.pawn_selecter=entity
                        board.moves_selecter=board.getMoves(entity,position)
                    else:
                        board.pawn_selecter=None
                        board.moves_selecter=[]
                else:
                    board.pawn_selecter=None
                    board.moves_selecter=[]
