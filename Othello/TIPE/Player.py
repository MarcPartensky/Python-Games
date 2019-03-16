from copy import deepcopy

import time
import random
import json
import ia
import config as cfg
import pygame

#

class Player:
    def __init__(self):
        self.choix=None


class Robot(Player):
    def __init__(self):
        Player.__init__(self)

    def jouer(self,plateau,fenetre):
        return self.randomPlay(plateau)
        #return ia.main(plateau)

    def old_jouer(self,input,plateau,fenetre):
         return self.randomPlay(plateau)

    def randomPlay(self,board):
        self.choix=random.choice(board.mouvements)
        return self.choix



    def smartPlay(self,board):
        mouvements=board.mouvements
        for mouvement in mouvements:
            pass




class Human(Player):
    def __init__(self):
        Player.__init__(self)


    def old_jouer(self,input,board,fenetre):
        click,cursor=input
        if click:
            position=board.adjust(cursor,fenetre)
            if board.est_dans_grille(position):
                if position in board.mouvements:
                    self.choix=position
        return self.choix

    def jouer(self,plateau,fenetre):
        while True :
            fenetre.check()
            cfg.debug(fenetre.point())
            cfg.debug(plateau,bool(pygame.mouse.get_pressed()[0]))
            if bool(pygame.mouse.get_pressed()[0]):
                cfg.debug("on a clicke")
                position=plateau.adjust(fenetre.point(),fenetre)#Donne des coordonnées
                cfg.debug("position:",position)
                if plateau.est_dans_grille(position):
                    if position in plateau.mouvements:#On regarde si le clique est une possibilité porpose par le plateau
                        self.choix=position
                        break
            cfg.debug('while true du joueur huamin pour jouer')
        return self.choix
