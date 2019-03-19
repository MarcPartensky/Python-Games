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

import player as Joueur
import time
import pygame
from pygame.locals import *##todo
import config as cfg

from copy import deepcopy



class Othello:
    def __init__(self,fenetre,liste_joueur,affichage=True):
        self.nom="Othello"
        self.fenetre=fenetre
        self.fenetre.name=self.nom
        if affichage: self.fenetre.set()
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
        self.gagnant=None
        self.historique=[]
        self.affichage=affichage


    def __call__(self):
        self.afficher()
        #cfg.debug(self.joueurs)
        while self.fenetre.open and not self.plateau.gagne:
            self.fenetre.check()
            self.faireTour()
            self.plateau.testVictoire()
        self.afficherSceneFinale()
        #print("C'est la fin, pour le moment...")


    def afficherSceneFinale(self):
        """Afficher le resultat de la partie une fois qu'elle est terminee."""
        comptes=[]
        for i in range(len(self.joueurs)):
            comptes.append(sum([self.plateau.grille[y].count(i) for y in range(len(self.plateau.grille))]))
        #print("Comptes final:",comptes)
        self.gagnant=comptes.index(max(comptes)) #determine un gagnant meme si la partie n'est pas encore finie
        if self.affichage:
            self.afficher()

            self.plateau.testVictoire()
            if self.plateau.gagne:
                message="Joueur "+str(self.gagnant+1)+" gagne!"
            else: #to complete with moves counter
                message="Match Nul"
            position=list(self.fenetre.centerText(message))
            position[0]-=50
            taille=[int(len(message)*self.fenetre.taille_du_texte/2.7),70]
            self.fenetre.print(message,position,taille,color=couleur.NOIR,couleur_de_fond=couleur.BLANC)
            self.fenetre.flip()
            self.fenetre.pause()
            #Todo retourner menu principal

    def afficher(self):
        """Affiche tout : le plateau"""
        if self.affichage:
            self.fenetre.clear()
            self.plateau.afficher(self.fenetre)
            self.fenetre.flip()

    def faireTour(self) :
        """Faire un tour de jeu"""
        self.tour = self.state % self.plateau.nombre_joueurs
        joueur_actif=self.joueurs[self.tour]#joueur a qui c'est le tour
        self.plateau.mouvements=self.plateau.obtenirMouvementsValides(joueur_actif.side)#todo pas top
        self.afficher()
        self.state+=1
        if len(self.plateau.mouvements)>=1:#Si des moves sont possibles
            choix_du_joueur=joueur_actif.jouer(deepcopy(self.plateau),self.fenetre, self.tour)
            if not choix_du_joueur:
                return None
            self.plateau.placerPion(choix_du_joueur,joueur_actif.side)
            #if self.affichage: self.plateau.afficherAnimationPion(self.fenetre,choix_du_joueur)
            self.historique.append([self.plateau.grille,joueur_actif.side,choix_du_joueur])
        else :
            #Si aucun mouvement possible on demane l'avis du joueur_actif
            pass
