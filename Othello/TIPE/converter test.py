import board
from converter import Converter

print(Converter(board.Board.conquerir_ligne)())
print(Converter(board.Board.est_mouvement_valide_dans_ligne)())

#puissance=lambda x:2**int(math.log(x)/math.log(2))

#print(Converter(puissance)())
