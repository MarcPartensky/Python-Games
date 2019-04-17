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
import couleurs

from plateau import Plateau

import joueur as Joueur
import time
import pygame
from pygame.locals import *
from config import log #Utilisé pour débuguer rapidement
import config as cfg

from copy import deepcopy



class Othello:
    def __init__(self,joueurs,fenetre=None,theme=None):
        self.nom="Othello"
        self.joueurs=joueurs
        for compteur in range(len(self.joueurs)):
            self.joueurs[compteur].attribuerCote(compteur)# i.e. : self.joueurs[compteur].cote=compteur
        self.state=0
        self.gagnant=None
        self.historique=[]

        #Permet de simuler des parties sans fenetre pour des combats machine vs machine
        if fenetre:
            self.chargerFenetre(fenetre) #Charge une fenetre existante
            self.chargerTheme(theme) #Charge un theme même si celui-ci est None
            log("Fenetre et theme:",self.fenetre,self.theme)
            self.plateau=Plateau(theme=self.theme)
        else:
            self.fenetre=None
            self.plateau=Plateau()



    def chargerFenetre(self,fenetre):
        """Permet de charger la fenetre en supposant qu'elle ne soit pas None."""
        fenetre.name=self.nom #Donne un nom a la fenêtre.
        fenetre.set() #Charge la fenêtre créée.
        fenetre.couleur_de_fond=couleurs.VERT #Charge la couleur de fond par défaut.
        self.fenetre=fenetre

    def chargerTheme(self,theme):
        """Charge un theme peut importe si celui-ci est None"""
        if theme: #Si celui-ci existe, le définir.
            self.theme=theme
        else: #Sinon, le créer.
            couleur_grille=couleurs.NOIR #Crée la couleur de la grille.
            couleur_pieces=[couleurs.BLANC,couleurs.NOIR] #Crée la couleur des pieces.
            couleur_mouvement=couleurs.ROUGE #Crée la couleur des mouvements
            self.theme=[couleur_grille,couleur_pieces,couleur_mouvement]

    def __call__(self):
        """Boucle principale du jeu Othello."""
        if self.fenetre: self.afficher()
        while not self.plateau.estFini():
            if self.fenetre:
                self.fenetre.check()
                if not self.fenetre.open: break
                self.afficher()
            self.faireTour()
        self.fin()
        if self.fenetre:
            self.afficher()
            self.afficherSceneFinale()

    def fin(self):
        """Determine le gagnant de la partie a la fin du jeu."""
        jouable=self.plateau.estJouable()
        cote_gagnant=self.plateau.obtenirCoteGagnant()
        #Faire attention au fait que le plateau ne connait que des cotés, et à
        #aucun moment il ne possède les vrais joueurs comme attributs.
        #Effectivement, ce sont les joueurs qui utilise le plateau et non l'inverse.
        if cote_gagnant: self.gagnant=self.joueurs[cote_gagnant]

    def afficherSceneFinale(self):
        """Afficher le resultat de la partie une fois qu'elle est terminee.
        Ne peut être exécutée que si la fenetre existe."""
        if self.gagnant: #Si il existe un gagnant, l'afficher.
            message=str(self.gagnant)+" gagne!"
        else: #Sinon, afficher match nul.
            message="Match Nul"
        position=list(self.fenetre.centerText(message)) #Centre la position du message, ne fonctionne pas correctement.
        position[0]-=50 #Recentre correctement le message.
        taille=[int(len(message)*self.fenetre.taille_du_texte/2.7),70] #Choisie la taille du message.
        self.fenetre.print(message,position,taille,color=couleurs.NOIR,couleur_de_fond=couleurs.BLANC) #Affiche le message.
        self.fenetre.flip() #Rafraîchie la fenêtre.
        self.fenetre.pause() #Fais pause en attendant que l'utilisateur appuie sur espace ou escape.

    def afficher(self):
        """Affiche tout : le plateau"""
        self.fenetre.clear()
        self.plateau.afficher(self.fenetre)
        self.fenetre.flip()

    def faireTour(self) :
        """Faire un tour de jeu"""
        self.tour = self.state % self.plateau.nombre_de_joueurs
        joueur_actif=self.joueurs[self.tour]#joueur a qui c'est le tour
        self.plateau.mouvements=self.plateau.obtenirMouvementsValides(self.tour)#todo pas top
        self.state+=1
        if len(self.plateau.mouvements)>=1:#Si des moves sont possibles
            choix_du_joueur=joueur_actif.jouer(deepcopy(self.plateau),self.fenetre)
            if not choix_du_joueur:
                return None
            self.plateau.placerPion(choix_du_joueur,joueur_actif.cote)
            self.plateau.afficherAnimationPion(self.fenetre,choix_du_joueur)
            self.historique.append([self.plateau.grille,joueur_actif.cote,choix_du_joueur]) #Permet en théorie au joueur de retourner en arrière.
        else :
            #Sinon aucun mouvement n'est possible et on passe uniquement au tour suivant
            pass
