from player import Player

import config as cfg
import random

class Ia(Player):
    def __init__(self):
        """Creer une instance de joueur."""
        super().__init__()

    def jouer(self):
        """Joue."""
        pass

    def jouerAleatoire(self,plateau):
        """Joue aleatoirement dans le plateau."""
        mouvements=plateau.obtenirMouvementsValides()
        return random.choice(mouvements)

    def compterPions(self,plateau,cote=None):
        """Compte les pions de tel couleur, par defaut compte ses propres pions."""
        cote=self.cote
        pions=plateau.obtenirPions(cote)
        return len(pions)

    def obtenirLignes(self,plateau,cote):
        """Renvoie la liste de toutes les lignes de pions de la meme couleur sur le plateau avec le côté du joueur en utilisant par defaut le cote du joueur actif."""
        """Chaque ligne est caractérisée par les pions situés aux extrémités et seules les lignes maximum sont comptées."""
        """Exemple: [((l1x1,l1y1),(l1x2,l1y2)),((l2x1,l2y1),(l2x2,l2y2))] contient les positions de 2 lignes l1 et l2."""
        lignes=[]
        tx,ty=plateau.taille
        for y in range(ty):
            for x in range(tx):
                position=(x,y)
                case=self.obtenirCase(position)
                directions=plateau.obtenirDirections()
                for direction in directions:
                    ligne=plateau.obtenirLigne(direction,position)
                    for position in ligne:
                        if case:
                            pass

    def obtenirLignesVerticales(self,plateau,cote):
        """Renvoie la liste de toutes les lignes verticales du plateau."""
        lignes=[]
        tx,ty=plateau.taille
        for x in range(tx):
            position=(x,0)
            direction=(0,1)
            ligne=plateau.obtenirLigne(direction,position)
            lignes.append(ligne)
        return lignes



    def obtenirCarres(self,plateau,cote):
        """Renvoie l'ensemble des carrés de pions dans le plateau qui appartiennent au joueur du côté 'cote'."""
        pass #A compléter

    def obtenirTriangles(self,plateau,cote):
        """Renvoie la liste des triangles de pions dans le plateau qui appartiennent au joueur du côté 'cote'."""
        pass #A compléter
