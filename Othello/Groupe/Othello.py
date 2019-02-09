"""#############################################################################
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
#                                SOMMAIRE
#
#    note : commenter le script correctement
#
#    0. Importation des librairie et Variable Globale  ......... ligne 36
#    1. Class Jeu (permet d'afficher le début) (temporaire)..... ligne 55
#    2.  ....................................................... ligne
#    3.  ....................................................... ligne
#    4.  ....................................................... ligne
#    5.  ....................................................... ligne
#    6.  ....................................................... ligne
#    7.  ....................................................... ligne
#    8.  ....................................................... ligne
#    9.  ....................................................... ligne
############################################################################"""
# -*-coding:utf-8-*-

import pygame
from pygame.locals import *
#from my_colors import *
from plateau import Plateau # faire la class fenêtre avant de pouvoir l'importer


vert=(0,255,0)
rouge=(255,0,0)
bleu=(0,0,255)
blanc=(255,255,255)
noir=(0,0,0)

######################
#  Variable Globale  #
######################

dimensions_plateau = 8      # permet la proportionnalité entre les objets

# résolution de l'écran
x_max,y_max = 800,800       # multiple de "dimensions_plateau" si possible
resolution = (x_max,y_max)  # t-uple contenant les dimensions de la fenêtre

########################
#  Variable Booléenne  #
########################

terminer = False


class Jeu:
    """
    CLASSE DU JEU IN-GAME:

    Ce quelle fait:
        - crée la fenêtre de jeu
        - Afficher le plateau de début de jeu avec 4 Pions centré
        - possède une grille de coordonnée (de 0 à 7) pour les 64 position possible des pions

    Fonction disponible:
        - showcircle() modélise la nouvelle grille (case vide=0, pion blanc=1, pion noir=2)
        - AfficherPlateau(self):
        - AfficherPions(self):
        - Attendre(self):       (attent une action de l'utilisateur pour la traiter)
    """
    def __init__(self):
        pygame.init()
        # crée une fenêtre
        #self.window=Window(resolution)

        self.ecran = pygame.display.set_mode(resolution)
        icon = pygame.image.load('icon.png')
        pygame.display.set_icon(icon)
        pygame.display.set_caption("Othello de marc le bolosse x) et de valentin") #valentin est un bolosse


        # affiche la grille de départ
        self.grille=[[0 for i in range(dimensions_plateau)] for i in range(dimensions_plateau)]
        self.grille[dimensions_plateau//2-1][dimensions_plateau//2-1]=1 #place le pion blanc
        self.grille[dimensions_plateau//2-1][dimensions_plateau//2]=2 #place le pion noir
        self.grille[dimensions_plateau//2][dimensions_plateau//2-1]=2 #place le pion noir
        self.grille[dimensions_plateau//2][dimensions_plateau//2]=1 #place le pion blanc

        self.jeu = True

    def AfficherPlateau(self):
        """Affiche le Plateau """
        self.ecran.fill(vert) # fond vert
        for k in range(1,dimensions_plateau+1): # trace le quadrillage
            pygame.draw.line(self.ecran,noir,[k*x_max//dimensions_plateau , 0],[k*x_max//dimensions_plateau , y_max],3)
            pygame.draw.line(self.ecran,noir,[0 , k*y_max//dimensions_plateau],[x_max , k*y_max//dimensions_plateau],3)
        if dimensions_plateau == 8:
            pygame.draw.circle(self.ecran,noir,[2*x_max//dimensions_plateau,2*y_max//dimensions_plateau],7)
            pygame.draw.circle(self.ecran,noir,[6*x_max//dimensions_plateau,2*y_max//dimensions_plateau],7)
            pygame.draw.circle(self.ecran,noir,[2*x_max//dimensions_plateau,6*y_max//dimensions_plateau],7)
            pygame.draw.circle(self.ecran,noir,[6*x_max//dimensions_plateau,6*y_max//dimensions_plateau],7)
        self.AfficherPions()

    def AfficherPions(self):
        """Redessine les pions correspondant au nouveau plateau"""
        for y in range(dimensions_plateau):
            for x in range(dimensions_plateau):
                case = self.grille[y][x]
                position=(int((x+1/2)*x_max/dimensions_plateau),int((y+1/2)*y_max/dimensions_plateau))
                if case == 1:
                    pygame.draw.circle(self.ecran,blanc,position,int(0.4*x_max//dimensions_plateau))
                if case ==2:
                    pygame.draw.circle(self.ecran,noir,position,int(0.4*x_max//dimensions_plateau))
        pygame.display.flip()

    def Attendre(self):
        """Attend un événement (en boucle infini) puis la traite"""
        action = False
        while (not action):
            keys=pygame.key.get_pressed()
            if keys[K_ESCAPE]:
                action = True
            # si on appuis sur la touche "r" on re-affiche le plateau (restart)
            elif keys[K_r]:
                action = True
                self.AfficherPlateau()
            for event in pygame.event.get():
                # si on quitte le programme
                if event.type == pygame.QUIT:
                    action = True
                    self.jeu = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        action = True
                        self.jeu = False
                # on récupère événement
                elif event.type == pygame.MOUSEBUTTONUP:
                    """
                    cette partie doit traiter de la modification du plateau,
                    des coup autoriser, etc
                    """
                    action = True
                    pos_x = event.pos[0]
                    pos_y = event.pos[1]

                    pygame.draw.circle(self.ecran,rouge,event.pos,40) # permet le debug

    def __call__(self): #Boucle principale
        # affiche le plateau
        self.AfficherPlateau()

        # boucle du jeu
        while(self.jeu is not terminer): # terminer = False
            self.Attendre()
            self.AfficherPions()



# crée une partie/fenêtre et lance le jeu
partie=Jeu()
partie()
