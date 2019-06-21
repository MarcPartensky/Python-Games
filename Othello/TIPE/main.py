from mywindow import Window
from othello import Othello
from joueur import Robot,Humain,Developpeur
from bruteforce import BruteForce

import ia
import ia2

"""
A faire:

FAire API pour IA avec des fonctions 'basique' comme :
Replacer les grille[y][x] par des grille[x][y]

Faire la methode  colorer_case dans board.py

faire ia basique : gestion des priorites : structure

Penser à faire une class "Coup" ou "Mouvement" qui prend un parametre une pos, une couleur

La plupart des methode de board.py qui retourne une liste de coo, retourne une liste de liste : autrement dit, les coo sont dans des liste et non des tuples => il faut chager ca et mettre les coo dans des tuples


Pour marc :9
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


if __name__=="__main__": #Ceci est exécuté uniquement si le fichier est exécuté directement et non depuis un autre fichier.

    fenetre=Window(taille=[800,800],set=False,fullscreen=False) #Crée une fenêtre.

    developpeur1=Developpeur()
    developpeur2=Developpeur()
    humain=Humain() #Crée un humain.
    machine1=ia.IA() #Crée une intelligence artificielle.
    machine2=ia2.IA()
    machine3=ia2.IA()
    bruteforce=BruteForce(level=3) #Crée une machine utilisant la force de calcul de la machine, cela est utile pour les tests de niveau des nouvelles intelligences artificielles.

    jeu=Othello(joueurs=[humain,bruteforce],fenetre=fenetre) #Crée un jeu.
    jeu() #Lance le jeu.
