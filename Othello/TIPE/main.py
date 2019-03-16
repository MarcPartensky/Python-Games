import Othello
import mywindow
import Player as Joueur

"""
TOdo :
FAire API pour IA avec des fonctions 'basique' comme :
Replacer les grille[y][x] par des grille[x][y]
Faire la metohde  colorer_case dans board.py

Pour marc :

"""


if __name__=="__main__":
    fenetre=mywindow.Window([800,800],set=False)
    jeu=Othello.Othello(fenetre, [Joueur.Human(),Joueur.Human()])
    #jeu=Othello.Othello(fenetre, [Joueur.Robot(),Joueur.Robot()])
    jeu()
