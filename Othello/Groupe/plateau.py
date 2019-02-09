import pygame
from my_colors import *

class Plateau:
    def __init__(self,taille = (8,8)):
        """Crée un plateau et charge ses attributs."""
        self.taille = taille
        self.grille = self.ChargerGrille(self.taille)
        self.couleurs = [blanc,noir]
        self.joueur=1

    def ChargerGrille(self,taille):
        """
        Crée la grille de case du plateau qui permetra de savoir que contient la case
        0 = case vide
        1 = pion blanc
        2 = pion noir
        """
        l,h=taille # longueur et hauteur
        grille = [[0 for x in range(taille[0])] for y in range(taille[1])]
        grille[h//2-1][l//2-1] = 1   # place le pion blanc
        grille[h//2-1][l//2]   = 2   # place le pion noir
        grille[h//2][l//2-1]   = 2   # place le pion noir
        grille[h//2][l//2]     = 1   # place le pion blanc
        return grille

    def RecupererPions(self,joueur):
        sx,sy=self.taille
        list=[]
        for y in range(sy):
            for x in range(sx):
                if self.grille[y][x]==joueur:
                    list.append((x,y))
        return list

    def RecupererMouvements(self,joueur):
        autour=[(x,y) for x in range(-1,2) for y in range(-1,2) if (x,y)!=(0,0)]
        ennemi=joueur%2+1
        coups_possibles=[]
        positions_ennemis=self.RecupererPions(ennemi)
        for position in positions_ennemis:
            pass




        return coups_possibles

    def Afficher(self,fenetre):
        """Affiche la grille et les pions."""
        self.AfficherGrille(fenetre)
        self.AfficherPions(fenetre)
        pygame.display.flip()

    def AfficherGrille(self,fenetre): # fenêtre a une taille et un écran
        """Affiche la grille."""
        l,h=self.taille
        self.ecran.fill(vert) # fond vert
        fl,fh=fenetre.taille
        for x in range(l): # ligne verticale
            pygame.draw.line(fenetre.ecran,noir,[(x+1)*fl//l , 0],[(x+1)*fl//h , fl//l],3)
        for y in range(h): # ligne horizontale
            pygame.draw.line(fenetre.ecran,noir,[0 , (y+1)*fh//h],[fh//h , (y+1)*fh//l],3)
        if self.taille == (8,8): # mini cercle au coin du carrée centrale de case 4x4 dans le plateau 8x8
            pygame.draw.circle(fenetre.ecran,noir,[2*fl//l,2*fh//h],7)
            pygame.draw.circle(fenetre.ecran,noir,[6*fl//l,2*fh//h],7)
            pygame.draw.circle(fenetre.ecran,noir,[2*fl//l,6*fh//h],7)
            pygame.draw.circle(fenetre.ecran,noir,[6*fl//l,6*fh//h],7)

    def AfficherPions(self,fenetre):
        """Redessine les pions correspondant au nouveau plateau"""
        l,h=self.taille
        fl,fh=fenetre.taille
        for y in range(h):
            for x in range(l):
                case = self.grille[y][x]
                position=(int((x+1/2)*fl/l),int((y+1/2)*fh/h))
                if case == 1:
                    pygame.draw.circle(fenetre.ecran,blanc,position,int(0.4*fl//l))
                if case == 2:
                    pygame.draw.circle(fenetre.ecran,noir,position,int(0.4*fl//l))
