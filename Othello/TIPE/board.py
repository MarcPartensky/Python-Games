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
#                           SOMMAIRE du plateau
#
#    note : commenter le script correctement
#
#    0.  __init__   ................................................ ligne  64
#    1.  creerGrille   ............................................. ligne  74
#    2.  est_dans_grille   ......................................... ligne  83
#    3.  est_un_coin   ............................................. ligne  89
#    4.  adjust   .................................................. ligne  96
#    5.  testVictoire   ............................................ ligne 103
#    6.  obtenirPositionsPions   ................................... ligne 112
#    7.  obtenirPions   ............................................ ligne 116
#    8.  obtenirEnvironnement   .................................... ligne 130
#    9.  insererPion   ............................................. ligne 145
#   10.  reverse_pion   ............................................ ligne 150
#   11.  obtenir_case   ............................................ ligne 158
#   12.  placer_pion   ............................................. ligne 163
#   13.  est_une_case_vide   ....................................... ligne 168
#   14.  est_une_case_joueur_side   ................................ ligne 172
#   15.  obtenirCotesEnnemis   ..................................... ligne 176
#   16.  obtenir_mouvements_valides   .............................. ligne 180
#   17.  estMouvementValide   ...................................... ligne 191
#   18.  estMouvementValideDansLigne   ............................. ligne 202
#   19.  conquerir   ............................................... ligne 220
#   20.  obtenirLigne   ............................................ ligne 228
#   21.  conquerir_ligne   ......................................... ligne 239
#   22.  manger   .................................................. ligne 256
#   24.  afficher   ................................................ ligne 261
#   25.  colorerCase   ............................................. ligne 267
#   26.  afficherMouvements   ...................................... ligne 273
#   27.  afficherGrille   .......................................... ligne
#   28.  afficherPions   ........................................... ligne
#
###############################################################################
"""
# --coding:utf-8--

from outils import intersection
import mycolors as couleur
import config as cfg

import pygame

class Board:
    def __init__(self,theme,nombre_joueurs=2,taille=[8,8]):
        """Cree un plateau"""
        self.theme=theme
        self.taille=taille
        self.creerGrille()
        self.couleur_grille,self.pieces_couleur,self.mouvements_couleur=theme
        self.mouvements=[]
        self.gagne=False
        self.taille_x,self.taille_y=self.taille
        self.nombre_joueurs=nombre_joueurs

    def creerGrille(self):
        """Cree une grille"""
        sx,sy=self.taille
        self.grille=[[cfg.CASE_VIDE for x in range(sx)] for y in range(sy)]
        self.insererPion([3,3],0)
        self.insererPion([3,4],1)
        self.insererPion([4,3],1)
        self.insererPion([4,4],0)

    def estDansGrille(self,position):
        """Verifie si la position est dans la grille"""
        sx,sy=self.taille
        x,y=position
        return (0<=x<sx and 0<=y<sy)

    def estCoin(self, position):
        """Determine si une position correspond a un coin."""
        x,y=position
        sx,sy=self.taille
        x_=x%(sx-1)
        y_=y%(sy-1)
        return (x_, y_)==(0,0)

    def adjust(self,position_brute,fenetre):
        """Converti les coordonnees du curseur pour obtenir les coordonnees de la case selectionnee"""
        wsx,wsy=fenetre.taille
        sx,sy=self.taille
        rx,ry=position_brute
        return (int(rx*sx/wsx),int(ry*sy/wsy))

    def testVictoire(self):
        """Test la victoire. pas au point"""
        #fonction incomplete car ne prends pas en compte le cas particulier dans lequel les joueurs n'ont aucun mouvement possible.
        compteur=cfg.CASE_VIDE
        for colonne in self.grille:
            compteur+=colonne.count(cfg.CASE_VIDE)
        self.gagne=(compteur==cfg.CASE_VIDE)
        return self.gagne

    def obtenirPositionsPions(self):
        """Renvoie la liste de la positione de tout les pions"""
        return self.obtenirPions(range(self.nombres_joueurs))

    def obtenirPions(self,cotes):
        """Obtenir toute les position de toutes les pieces de cotes de joueurs"""
        if not isinstance(cotes,list):
            cotes=[cotes]
        positions=[]
        for cote in cotes:
            sx,sy=self.taille
            for y in range(sy):
                for x in range(sx):
                    case=self.obtenirCase([x,y])
                    if self.estCaseJoueur([x,y],cote):
                        positions.append([x,y])
        return positions

    def obtenirEnvironnement(self,positions):
        """Prend en parametre une liste de position de case et retourne la liste des postions des cases vide se trouvant juste à cote"""
        environnement=[]
        directions=[(x,y) for x in range(-1,2) for y in range(-1,2) if (x,y)!=(0,0)]
        for position in positions:
            px,py=position
            for pas in directions:
                stx,sty=pas
                x,y=(px+stx,py+sty)
                if self.estDansGrille([x,y]):
                    if self.estCaseVide([x,y]) :
                        environnement.append([x,y])
        print(1,environnement)
        environnement=list(intersection(environnement))
        print(2,environnement)
        return environnement

    def insererPion(self, coordonnees, side) :
        """insererPion insere un pion dans la grille sans se soucier de conquerir le territoire"""
        x,y=coordonnees
        self.grille[y][x]=side

    def reverse_pion(self, coordonnees): #ne peux pas marcher si on considere un jeu avec plus de 2 joueurs.
        """Retourne le pion se trouvant au coordonnees"""
        x,y=coordonnees
        #self.grid[y][x]=
        #Todo pour marc : faire cette fonction
        #Utiliser cette methode dans la methode 'conquer'
        pass

    def obtenirCase(self,coordonnees):
        """Retourne le contenu d'une case"""
        x,y=coordonnees
        return self.grille[y][x]

    def placerPion(self,coordonnees_pion,side):
        """Place un pion sur le plateau"""
        self.insererPion(coordonnees_pion, side)
        self.conquerir(coordonnees_pion,side)

    def estCaseVide(self, position):
        """Determine si la case a la position donnee est une case vide."""
        return self.obtenirCase(position)==cfg.CASE_VIDE

    def estCaseJoueur(self,position,cote):
        """Determine si la case a la position donnee contient un pion du joueur side."""
        return self.obtenirCase(position)==cote

    def obtenirCotesEnnemis(self,joueur_cote):
        """Renvoie la liste des cotes enemis d'un cote de joueur."""
        return [cote for cote in range(self.nombre_joueurs) if cote!=joueur_cote]

    def obtenir_mouvements_valides(self,joueur_cote): #yavait fenetre dans les parametres
        """Retourne une liste de tuple qui correspondent aux coordonnees des mouvements possibles pour le joueur_side"""
        cotes=self.obtenirCotesEnnemis(joueur_cote)
        positions=self.obtenirPions(cotes)
        cfg.debug(positions)
        positions_possibles=self.obtenirEnvironnement(positions)
        mouvements_valides=[]
        for position_possible in positions_possibles:
            if self.estMouvementValide(position_possible,joueur_cote):
                mouvements_valides.append(position_possible)
        return mouvements_valides

    def estMouvementValide(self,mouvement,cote):
        """Permet de verifier si un mouvement est valide."""
        vecteurs=[(x,y) for x in range(-1,2) for y in range(-1,2) if (x,y)!=(0,0)]
        resultat=False
        for vecteur in vecteurs:
            ligne=self.obtenirLigne(vecteur,mouvement)
            if self.estMouvementValideDansLigne(cote,ligne):
                resultat=True
                break
        return resultat

    def estMouvementValideDansLigne(self,p_side,ligne):
        """Permet de verifier si un mouvement est valide dans une ligne."""
        e_side=1-p_side
        valide=True
        possible=False
        for position in ligne:
            if not self.est_dans_grille(position):
                break
            case=self.obtenir_case(position)
            if case==e_side:
                possible=True
            elif case==p_side and possible:
                valide=True
                break
            else: #Dans ce case la case est vide
                break
        return valide

    def conquerir(self,position,p_side):
        """Permet au nouveau pion à la position 'position' de couleur 'side' de
        retouner les autres pions"""
        vecteurs=[(x,y) for x in range(-1,2) for y in range(-1,2) if (x,y)!=(0,0)]
        for vecteur in vecteurs:
            ligne=self.obtenir_ligne(vecteur,position)
            self.conquerir_ligne(p_side,ligne)

    def obtenirLigne(self,position,vecteur):
        """Recupere la ligne des valeurs obtenue avec une position et un vecteur."""
        line=[]
        vx,vy=vecteur
        x,y=position
        while self.estDansGrille((x,y)):
            x+=vx
            y+=vy
            line.append((x,y))
        return line

    def conquerir_ligne(self,p_side,ligne):
        """Permet au nouveau pion a la position position de couleur side de
        retouner les autres pions dans une ligne"""
        e_side=1-p_side
        mangeables=[]
        for position in ligne:
            if not self.est_dans_grille(position):
                break
            case=self.obtenir_case(position)
            if case==e_side:
                mangeables.append(position)
            elif case==p_side:
                self.manger(mangeables,p_side)
                break
            else: #Dans ce case la case est vide
                break

    def manger(self,mangeables,personne):
        """Assigne aux cases mangeables la valeur de pion de la personne"""
        for mangeable in mangeables:
            self.insererPion(mangeable,personne)

    def afficher(self,fenetre):
        self.afficherGrille(fenetre)
        #self.afficherDecorationGrille(fenetre)
        self.afficherPions(fenetre)
        self.afficherMouvements(fenetre)

    def colorerCase(postion, couleur) :
        """permet de colorer une case du plateau d'une certaine couleur
        cette fonction est utile pour debug de ia.py"""
        pass


    def afficherMouvements(self,fenetre,mouvements=None,couleur=None):
        """Afficher les coups possible. (point rouge sur la fenêtre)"""
        if not mouvements:
            mouvements=self.mouvements
        if not couleur:
            couleur=self.theme[2]
        #devrait  marcher si il n'y a que un moment.
        for move in mouvements:
            wsx,wsy=fenetre.taille
            sx,sy=self.taille
            radius=int(min(wsx,wsy)/min(sx,sy)/4)
            x,y=move
            raw_position=(int((x+1/2)*wsx/sx),int((y+1/2)*wsy/sy))
            pygame.draw.circle(fenetre.screen,couleur,raw_position,radius,0)


    def afficherGrille(self,fenetre):
        """Affiche la grille"""
        wsx,wsy=fenetre.taille
        sx,sy=self.taille
        for y in range(sy):
            _y=y*wsy//sy
            start=(0,_y)
            end=(wsx,_y)
            pygame.draw.line(fenetre.screen,self.couleur_grille,start,end,1)
        for x in range(sx):
            _x=x*wsx//sx
            start=(_x,0)
            end=(_x,wsy)
            pygame.draw.line(fenetre.screen,self.couleur_grille,start,end,1)

    def afficherPions(self,fenetre):
        """Affiche les pions"""
        wsx,wsy=fenetre.taille
        sx,sy=self.taille
        radius=int(min(wsx,wsy)/min(sx,sy)/2)
        for y in range(sy):
            for x in range(sx):
                case=self.obtenirCase((x,y))
                raw_position=(int((x+1/2)*wsx/sx),int((y+1/2)*wsy/sy))
                if 0<=case and case<=len(self.pieces_couleur)-1 :
                    couleur=self.pieces_couleur[case]
                    pygame.draw.circle(fenetre.screen,couleur,raw_position,radius,0)
