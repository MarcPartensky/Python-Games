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
#                           SOMMAIRE de Othello
#
#    note : commenter le script correctement
#
#    0. __init__   ................................................ ligne
#    1. __call__   ................................................ ligne
#    2. finalScene   .............................................. ligne
#    3. getInput   ................................................ ligne
#    4. afficher   ................................................ ligne
#    5. faireTour   ............................................... ligne
#
###############################################################################
"""
# --coding:utf-8--

import mywindow
import mycolors as couleur

import board as Plateau

import Player as Joueur
import time
import pygame
from pygame.locals import *##todo
import config as cfg

from copy import deepcopy



class Othello:
    def __init__(self,fenetre, liste_joueur):
        self.nom="Othello"
        self.fenetre=fenetre
        self.fenetre.name=self.nom
        self.fenetre.set()
        self.fenetre.couleur_de_fond=couleur.VERT
        self.couleur_grille=couleur.NOIR
        self.couleur_pieces=[couleur.BLANC,couleur.NOIR]
        self.couleur_mouvement=couleur.ROUGE
        self.theme=[self.couleur_grille,self.couleur_pieces,self.couleur_mouvement]
        self.joueurs=liste_joueur
        for compteur in range(len(self.joueurs)):
            self.joueurs[compteur].side=compteur
        self.plateau=Plateau.Board(self.theme,len(self.joueurs))
        self.state=0
        self.tour=self.state%self.plateau.nombre_joueurs


    def __call__(self):
        self.afficher()

        #cfg.debug(self.joueurs)
        while self.fenetre.open and not self.plateau.gagne:
            self.fenetre.check()
            self.faireTour()
            self.plateau.testVictoire()
        self.finalScene()
        print("c'est la fin")


    def finalScene(self):
        """Afficher le resultat de la partie une fois qu'elle est terminee."""
        #self.afficher()
        self.tour = self.state % self.nombre_joueurs
        joueur_actif=self.joueurs[self.tour]
        if self.gagne:
            message="Joueur "+str(joueur_actif.side+1)+" won!"
        if not self.gagne: #to complete with moves counter
            message="Match Nul"
        position=list(self.fenetre.centerText(message))
        position[0]-=50
        taille=[int(len(message)*self.fenetre.taille_du_texte/2.7),70]
        self.fenetre.print(message,position,taille,color=couleur.NOIR,couleur_de_fond=couleur.BLANC)
        self.fenetre.flip()
        while self.fenetre.open:
            self.fenetre.check()#On attend qu'on ferme la fenetre
        #Todo retourner menu principal

    def getInput(self):
        """Actualise les parametre du jeu, ou se trouve le curseur, est-ce qu'on clique ?"""
        entree=self.entree
        while (entree is self.entree) and self.fenetre.open:
            self.fenetre.check()
            click=self.fenetre.click()
            curseur=self.fenetre.point()
            entree=(click,curseur)
        self.entree=entree
        return self.entree

    def afficher(self):
        """Affiche tout : le plateau"""
        self.fenetre.clear()
        self.plateau.afficher(self.fenetre)
        self.fenetre.flip()

    def faireTour(self) :
        """Faire un tour de jeu"""
        self.tour = self.state % self.plateau.nombre_joueurs
        joueur_actif=self.joueurs[self.tour]#joueur a qui c'est le tour
        self.plateau.mouvements=self.plateau.obtenir_mouvements_valides(joueur_actif.side)#todo pas top
        #cfg.debug(self.plateau.mouvements)
        self.afficher()
        self.state+=1
        if len(self.plateau.mouvements)>=1:#Si des moves sont possibles
            choix_du_joueur=joueur_actif.jouer(deepcopy(self.plateau),self.fenetre, self.tour)
            if not choix_du_joueur:
                return None

            self.plateau.placerPion(choix_du_joueur, joueur_actif.side)
        else :
            #Si aucun mouvement possible on demane l'avis du joueur_actif
            pass
