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
#   16.  obtenirMouvementsValides   .............................. ligne 180
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
import outils
from outils import linearBijection as bijection
import mycolors as couleur
import config as cfg
import time #pour les animations
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
        return [x_,y_]==[0,0]

    def adjuster(self,position_brute,fenetre):
        """Converti les coordonnees du curseur pour obtenir les coordonnees de la case selectionnee"""
        wsx,wsy=fenetre.taille
        sx,sy=self.taille
        rx,ry=position_brute
        return [int(rx*sx/wsx),int(ry*sy/wsy)]

    def testVictoire(self):
        """Test la victoire. pas au point"""
        #fonction incomplete car ne prends pas en compte le cas particulier dans lequel les joueurs n'ont aucun mouvement possible.
        compteur=0
        for colonne in self.grille:
            compteur+=colonne.count(cfg.CASE_VIDE)
        if compteur==0: #Verifie si il reste encore des cases vides
            self.gagne=True
            return self.gagne
        else: #S'il en reste, verifie si au moins un joueur peut joueur
            self.gagne=True
            for i in range(self.nombre_joueurs):
                validite=len(self.obtenirMouvementsValides(i))>0
                if validite:
                    self.gagne=False
                    break
        return self.gagne

    def obtenirPositionsPions(self):
        """Renvoie la liste de la positione de tout les pions"""
        return self.obtenirPions(range(self.nombre_joueurs))


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

    def obtenirNombrePionsJoueur(self, cote):#Todo à optimiser
        nombre=0
        sx, sy = self.taille
        for y in range(sy):
            for x in range(sx):
                if self.estCaseJoueur((x,y), cote) :
                    nombre+=1
        return nombre


    def obtenirEnvironnement(self,positions):
        """Prend en parametre une liste de position de case et retourne la liste des postions des cases vide se trouvant juste à cote"""
        environnement=[]
        directions=[[x,y] for x in range(-1,2) for y in range(-1,2) if [x,y]!=[0,0]]
        for position in positions:
            px,py=position
            for pas in directions:
                stx,sty=pas
                x,y=(px+stx,py+sty)
                if self.estDansGrille([x,y]):
                    if self.estCaseVide([x,y]) :
                        environnement.append([x,y])
        environnement=list(outils.intersection_(environnement))
        return environnement

    def insererPion(self,positions,cote) :
        """insererPion insere un pion dans la grille sans se soucier de conquerir le territoire"""
        if len(positions)>0:
            if type(positions[0])==list:
                for position in positions:
                    x,y=position
                    self.grille[y][x]=cote
            else:
                x,y=positions
                self.grille[y][x]=cote

    def obtenirCase(self,coordonnees):
        """Retourne le contenu d'une case"""
        x,y=coordonnees
        return self.grille[y][x]

    def placerPion(self,position,cote):
        """Place un pion sur le plateau"""
        self.insererPion(position,cote)
        return self.conquerir(position,cote)

    def estCaseVide(self, position):
        """Determine si la case a la position donnee est une case vide."""
        return self.obtenirCase(position)==cfg.CASE_VIDE

    def estCaseJoueur(self,position,cote):
        """Determine si la case a la position donnee contient un pion du joueur side."""
        return self.obtenirCase(position)==cote

    def obtenirCotesEnnemis(self,joueur_cote):
        """Renvoie la liste des cotes enemis d'un cote de joueur."""
        return [cote for cote in range(self.nombre_joueurs) if cote!=joueur_cote]

    def obtenirMouvementsValides(self,joueur_cote): #yavait fenetre dans les parametres
        """Retourne une liste de tuple qui correspondent aux coordonnees des mouvements possibles pour le joueur_side"""
        cotes=self.obtenirCotesEnnemis(joueur_cote)
        positions=self.obtenirPions(cotes)
        #cfg.debug(positions)
        positions_possibles=self.obtenirEnvironnement(positions)
        #cfg.debug(positions_possibles)
        mouvements_valides=[]
        for position_possible in positions_possibles:
            if self.estMouvementValide(position_possible,joueur_cote):
                mouvements_valides.append(position_possible)
        return mouvements_valides

    def estMouvementValide(self,mouvement,cote):
        """Permet de verifier si un mouvement est valide."""
        directions=[[x,y] for x in range(-1,2) for y in range(-1,2) if [x,y]!=[0,0]]
        #cfg.debug("directions:",directions)
        resultat=False
        for direction in directions:
            ligne=self.obtenirLigne(mouvement,direction)
            #cfg.debug("ligne:",ligne)
            validite=self.estMouvementValideDansLigne(cote,ligne)
            #cfg.debug("validite:",validite)
            if validite:
                resultat=True
                break
        return resultat

    def estMouvementValideDansLigne(self,cote,ligne):
        """Permet de verifier si un mouvement est valide dans une ligne."""
        valide=False
        possible=False
        for position in ligne:
            if not self.estDansGrille(position):
                break
            case=self.obtenirCase(position)
            if case!=cote and case!=cfg.CASE_VIDE:
                possible=True
            elif case==cote:
                if possible:
                    valide=True
                break
            else: #Dans ce case la case est vide
                break
        return valide

    def conquerir(self,position,p_side):
        """Permet au nouveau pion à la position 'position' de couleur 'side' de
        retouner les autres pions"""
        directions=[[x,y] for x in range(-1,2) for y in range(-1,2) if [x,y]!=[0,0]]
        for direction in directions:
            ligne=self.obtenirLigne(position,direction)
            self.conquerirLigne(p_side,ligne)
        return True

    def obtenirLigne(self,position,vecteur):
        """Recupere la ligne des valeurs obtenue avec une position et un vecteur."""
        line=[]
        vx,vy=vecteur
        #cfg.debug(position)
        x,y=position
        while self.estDansGrille([x,y]):
            x+=vx
            y+=vy
            line.append([x,y])
        return line

    def conquerirLigne(self,cote,ligne):
        """Permet au nouveau pion a la position position de couleur side de
        retouner les autres pions dans une ligne"""
        mangeables=[]
        for position in ligne:
            if not self.estDansGrille(position):
                break
            case=self.obtenirCase(position)
            if case!=cote and case!=cfg.CASE_VIDE:
                mangeables.append(position)
            elif case==cote:
                self.manger(mangeables,cote)
                break
            else: #Dans ce case la case est vide
                break

    def manger(self,mangeables,personne):
        """Assigne aux cases mangeables la valeur de pion de la personne"""
        self.insererPion(mangeables,personne)

    def afficher(self,fenetre):
        self.afficherFond(fenetre)
        self.afficherGrille(fenetre)
        #self.afficherDecorationGrille(fenetre)
        self.afficherPions(fenetre)
        self.afficherMouvements(fenetre)

    def colorerCase(postion, couleur) :
        """permet de colorer une case du plateau d'une certaine couleur
        cette fonction est utile pour debug de ia.py"""
        pass

    def afficherFond(self,fenetre):
        """Affiche un fond colore."""
        ftx,fty=fenetre.taille
        for y in range(0,fty,10):
            for x in range(0,ftx,10):
                r=abs(bijection(x,[0,ftx],[-100,100]))
                g=255-abs(bijection((x+y)/2,[0,ftx],[-100,100]))
                b=abs(bijection(y,[0,fty],[-100,100]))
                couleur=(r,g,b)
                fenetre.draw.rect(fenetre.screen,couleur,[x,y,10,10],0)


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
            fenetre.draw.circle(fenetre.screen,(100,0,0),raw_position,radius+2,0) #affiche des bord aux couleurs, bonne idees mais mal implemente
            fenetre.draw.circle(fenetre.screen,couleur,raw_position,radius,0)


    def afficherGrille(self,fenetre):
        """Affiche la grille"""
        wsx,wsy=fenetre.taille
        sx,sy=self.taille
        for y in range(sy):
            _y=y*wsy//sy
            start=(0,_y)
            end=(wsx,_y)
            fenetre.draw.line(fenetre.screen,self.couleur_grille,start,end,1)
        for x in range(sx):
            _x=x*wsx//sx
            start=(_x,0)
            end=(_x,wsy)
            fenetre.draw.line(fenetre.screen,self.couleur_grille,start,end,1)

    def afficherAnimationPion(self,fenetre,choix_du_joueur):
        wsx,wsy=fenetre.taille
        sx,sy=self.taille
        radius=int(min(wsx,wsy)/min(sx,sy)/2.5)
        x,y=choix_du_joueur
        raw_position=(int((x+1/2)*wsx/sx),int((y+1/2)*wsy/sy))
        case=self.obtenirCase(choix_du_joueur)
        couleur=self.pieces_couleur[case]
        for i in range(2):
            fenetre.draw.circle(fenetre.screen,couleur,raw_position,radius+2,0)
            fenetre.check()
            fenetre.flip()
            time.sleep(0.2)
            fenetre.draw.circle(fenetre.screen,(255,0,0),raw_position,radius+2,0) #tres mal implemente
            fenetre.draw.circle(fenetre.screen,couleur,raw_position,radius,0)
            fenetre.check()
            fenetre.flip()





    def afficherPions(self,fenetre):
        """Affiche les pions"""
        wsx,wsy=fenetre.taille
        sx,sy=self.taille
        radius=int(min(wsx,wsy)/min(sx,sy)/2.5) #taille des pions a changer
        for y in range(sy):
            for x in range(sx):
                case=self.obtenirCase([x,y])
                raw_position=(int((x+1/2)*wsx/sx),int((y+1/2)*wsy/sy))
                if 0<=case and case<=len(self.pieces_couleur)-1 :
                    couleur=self.pieces_couleur[case]
                    fenetre.draw.circle(fenetre.screen,fenetre.reverseColor(couleur),raw_position,radius+2,0)
                    fenetre.draw.circle(fenetre.screen,couleur,raw_position,radius,0)
