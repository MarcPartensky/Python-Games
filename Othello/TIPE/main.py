import othello
import mywindow
import player as Joueur

"""
TOdo :

obtenir_side_joueur_oppose => le board doit connaitre le nombre de joueur dans board.py

FAire API pour IA avec des fonctions 'basique' comme :
Replacer les grille[y][x] par des grille[x][y]

Faire la methode  colorer_case dans board.py

faire ia basique

debugage detecter correctement la fin de la partie => faire nouvelle methode dans board.oy et player.py
test vistoire dans le board.py

Pour marc :
Indiquer dans la fenetre à qui c'est le tour
faire plus de trucs chelous

La deco inutile à faire :
Mini animation pour indiquer le dernier pion posé : colorer ses rebord de la couleur NEW_COLOR_PIECES, à ajouter dans les constantes
Ajouter les 4 points noirs sur le plateau.
Ajouter un menu très basique=>nouvelle class est nouveau fichier .py

"""


if __name__=="__main__":
    fenetre=mywindow.Window(taille=[800,800],set=False)
    jeu=othello.Othello(fenetre, [Joueur.Robot(),Joueur.Robot()])
    #jeu=Othello.Othello(fenetre, [Joueur.Robot(),Joueur.Robot()])
    jeu()
