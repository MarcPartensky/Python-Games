import othello
import mywindow
from player import Robot,Humain
from ia import IA
#from beast import Beast

"""
TOdo :

obtenir_side_joueur_oppose => le board doit connaitre le nombre de joueur dans board.py

FAire API pour IA avec des fonctions 'basique' comme :
Replacer les grille[y][x] par des grille[x][y]

Faire la methode  colorer_case dans board.py

faire ia basique : gestion des priorites : structure

Penser à faire une class "Coup" ou "Mouvement" qui prend un parametre une pos, une couleur

La plupart des methode de board.py qui retourne une liste de coo, retourne une liste de liste : autrement dit, les coo sont dans des liste et non des tuples => il faut chager ca et mettre les coo dans des tuples


Pour marc :
Indiquer dans la fenetre à qui c'est le tour
La fonction board.conquerir doit renvoyer le nombre de pion retourne

La deco inutile à faire :
Mini animation pour indiquer le dernier pion posé : colorer ses rebord de la couleur NEW_COLOR_PIECES, à ajouter dans les constantes

Ajouter les 4 points noirs sur le plateau.
Ajouter un menu très basique=>nouvelle class est nouveau fichier .py

Pour dossier :
expliquer demarche dans cahier de bord
Faire mini schema des heritage de classe


"""


if __name__=="__main__":
    fenetre=mywindow.Window(taille=[900,900],set=False,fullscreen=True)
    #jeu=othello.Othello(fenetre, [Robot(),Beast()])
    jeu=othello.Othello(fenetre, [IA(),Humain()])
    jeu()
