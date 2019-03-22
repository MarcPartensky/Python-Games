import othello
import mywindow
import player as Joueur

"""
TOdo :

obtenir_side_joueur_oppose => le board doit connaitre le nombre de joueur dans board.py

FAire API pour IA avec des fonctions 'basique' comme :
Replacer les grille[y][x] par des grille[x][y]

Faire la methode  colorer_case dans board.py

faire ia basique : gestion des priorites : structure


Pour marc :
Indiquer dans la fenetre à qui c'est le tour

La deco inutile à faire :
Mini animation pour indiquer le dernier pion posé : colorer ses rebord de la couleur NEW_COLOR_PIECES, à ajouter dans les constantes

Ajouter les 4 points noirs sur le plateau.
Ajouter un menu très basique=>nouvelle class est nouveau fichier .py

Pour dossier :
expliuerdemarche dans cahier de bord
Faire mini schema des heritage de classe


"""


if __name__=="__main__":
    fenetre=mywindow.Window(taille=[800,800],set=False,fullscreen=True)
    jeu=othello.Othello(fenetre, [Joueur.Robot(),Joueur.Robot()])
    #jeu=Othello.Othello(fenetre, [Joueur.Robot(),Joueur.Robot()])
    jeu()
