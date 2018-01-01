"""
################################################################################
#
#              Institut Supérieur d'électronique de Paris (ISEP)
#
#                               SUJET DE TIPE:
#                     Othello et Intelligence Artificielle
#
#    Première année  --  MPSI
#
#    Créateurs : Marc  PARTENSKY
#                Valentin  COLIN
#                Alexandre Bigot
#
#    Version : 2019
#              1.1
#
###############################################################################
#
#                           SOMMAIRE de Player
#
#    note : commenter le script correctement
#
#    0. __init__   ................................................ ligne
#
###############################################################################
#
#                           SOMMAIRE de Humain
#
#    0. __init__   ................................................ ligne
#    1. old_jouer   ............................................... ligne
#    2. jouer   ................................................... ligne
#
###############################################################################
#
#                           SOMMAIRE de Robot
#
#    0. __init__   ................................................ ligne
#    1.jouer   ................................................... ligne
#    2. main   .................................................... ligne
#
###############################################################################
"""
# --coding:utf-8--

import time
import random
import json
import config as cfg
import pygame
import couleurs


class Joueur:
    def __init__(self):
        """Cree un joueur et défini son choix à rien. Il s'agit de la classe de base de tous les joueurs."""
        self.choix=None

    def attribuerCote(self,cote):
        """Défini le côté d'un joueur, celui-ci peut varier d'une partie à une autre."""
        self.cote=cote
        self.cote_oppose=1-self.cote

    def reinitialiser(self, plateau):
        #A compléter par Alexandre
        pass

    def __str__(self):
        """Renvoie une représentation du joueur en string."""
        #Habituellement le joueur ne connait pas sa couleur et ne possede pas de nom
        #mais ce celui-ci connait toujours son coté.
        #Effectivement c'est le plateau qui affiche une couleur prédéfinie dans le thème.
        if "nom" in self.__dict__: #Vérifie si le joueur possede un attribut nom
            text="Joueur"+str(self.name)
        elif "couleur" in self.__dict__: #Vérifie si le joueur possede un attribut couleur
            #Pourrait fonctionner si l'on créer une classe de couleur
            #mais c'est un peu exagéré.
            text="Joueur"+str(self.couleur)
        else: #Sinon dans la plupart des cas on affiche uniquement son côté.
            text="Joueur"+str(self.cote)
        return text

    __repr__=__str__ #Permet de faire un print et d'obtenir le même résultat que str.



class Humain(Joueur):
    def __init__(self):
        """Crée un humain qui hérite de joueur."""
        Joueur.__init__(self)  #Compatibilité avec python2.7 avec cette écriture théoriquement.

    def old_jouer(self,input,board,fenetre,cote):
        """Ancienne fonction obselète utilisée au début du jeu pour joueur."""
        click,cursor=input
        if click:
            position=board.adjust(cursor,fenetre)
            if board.estDansGrille(position):
                if position in board.mouvements:
                    self.choix=position
        return self.choix

    def jouer(self,plateau,fenetre):
        """Le joueur choisi un coup parmi ceux que le plateau lui propose et peux le sélectionner a l'aide de la fenêtre."""
        while fenetre.open:
            fenetre.check()
            curseur=fenetre.point()#Renvoie les coordonnees du curseur
            position=plateau.obtenirPositionPlateau(curseur,fenetre) #Transforme les coordonnees du curseur dans le systeme de coordonnees du plan
            plateau.afficher(fenetre)
            plateau.colorerCase(position,couleurs.BLEU,fenetre)
            fenetre.flip()
            click=fenetre.click()
            #print(click,position,plateau.mouvements)
            if click:
                if plateau.estDansGrille(position):
                    if position in plateau.mouvements: #On regarde si le clique est une possibilité propose par le plateau
                        self.choix=position
                        break
        return self.choix

    def __str__(self):
        """Renvoie une représentation du joueur en string."""
        #Habituellement le joueur ne connait pas sa couleur et ne possede pas de nom
        #mais ce celui-ci connait toujours son coté.
        #Effectivement c'est le plateau qui affiche une couleur prédéfinie dans le thème.
        if "nom" in self.__dict__: #Vérifie si le joueur possede un attribut nom
            text="Joueur"+str(self.name)
        elif "couleur" in self.__dict__: #Vérifie si le joueur possede un attribut couleur
            #Pourrait fonctionner si l'on créer une classe de couleur
            #mais c'est un peu exagéré.
            text="Joueur"+str(self.couleur)
        else: #Sinon dans la plupart des cas on affiche uniquement son type.
            text="Joueur Humain"
        return text

class Robot(Joueur):
    def __init__(self):
        """Cree un joueur robot qui hérite de joueur. Il s'agit de la classe de base de tous les robots."""
        Joueur.__init__(self) #Compatibilité avec python2.7 avec cette écriture théoriquement.

    def jouer(self,plateau,fenetre):
        """Le joueur renvoie un mouvement parmi les mouvements possibles a l'aide du plateau et de la fenetre."""
        return self.main(plateau)#todo verif si c'est bien possible

    def main(self, plateau):
        """"Methode à surcharger"""
        cfg.debug("Random actif, Robot.main n'a pas ete surcharge")
        return self.jouerAleatoire(plateau)

    def jouerAleatoire(self,board):
        """Le joueur choisi un des mouvements possibles aléatoirement."""
        self.choix=random.choice(board.mouvements)
        return self.choix

    def __str__(self):
        """Renvoie une représentation du joueur en string."""
        #Habituellement le joueur ne connait pas sa couleur et ne possede pas de nom
        #mais ce celui-ci connait toujours son coté.
        #Effectivement c'est le plateau qui affiche une couleur prédéfinie dans le thème.
        if "nom" in self.__dict__: #Vérifie si le joueur possede un attribut nom
            text="Joueur"+str(self.name)
        elif "couleur" in self.__dict__: #Vérifie si le joueur possede un attribut couleur
            #Pourrait fonctionner si l'on créer une classe de couleur
            #mais c'est un peu exagéré.
            text="Joueur"+str(self.couleur)
        else: #Sinon dans la plupart des cas on affiche uniquement son type.
            text="Joueur Robot"
        return text
