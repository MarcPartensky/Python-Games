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
#                           SOMMAIRE de Human
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

from copy import deepcopy

import time
import random
import json
#import ia
import config as cfg
import pygame

#

class Player:
    def __init__(self):
        self.choix=None

class Humain(Player):
    def __init__(self):
        Player.__init__(self)


    def old_jouer(self,input,board,fenetre,side):
        click,cursor=input
        if click:
            position=board.adjust(cursor,fenetre)
            if board.estDansGrille(position):
                if position in board.mouvements:
                    self.choix=position
        return self.choix

    def jouer(self,plateau,fenetre,side):
        while fenetre.open:
            fenetre.check()
            if bool(pygame.mouse.get_pressed()[0]):
                position=plateau.adjuster(fenetre.point(),fenetre)#Donne des coordonnées
                if plateau.estDansGrille(position):
                    if position in plateau.mouvements:#On regarde si le clique est une possibilité propose par le plateau
                        self.choix=position
                        break
        return self.choix

class Robot(Player):
    def __init__(self):
        Player.__init__(self)

    def jouer(self,plateau,fenetre,side):
        return self.randomPlay(plateau)
        #return self.main(plateau)#todo verif si c'est bien possible

    def main(self, plateau):
        """"Methode à surchager"""
        pass

    def old_jouer(self,input,plateau,fenetre,side):
        return self.randomPlay(plateau)

    def randomPlay(self,board):
        self.choix=random.choice(board.mouvements)
        return self.choix



    def smartPlay(self,board):
        mouvements=board.mouvements
        for mouvement in mouvements:
            pass
