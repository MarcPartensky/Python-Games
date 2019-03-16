import mycolors as couleur
import config as cfg

import pygame

class Board:
    def __init__(self,theme,taille=[8,8]):
        """Cree un plateau"""
        self.taille=taille
        self.createGrid()
        self.couleur_grille,self.pieces_couleur,self.mouvements_couleur=theme
        self.mouvements=[]
        self.gagne=False
        self.taille_x, self.taille_y =self.taille


    def createGrid(self):
        """Cree une grille"""
        sx,sy=self.taille
        self.grille=[[cfg.CASE_VIDE for x in range(sx)] for y in range(sy)]
        self.inserer_pion((3,3),0)
        self.inserer_pion((3,4),1)
        self.inserer_pion((4,3),1)
        self.inserer_pion((4,4),0)


    def est_dans_grille(self,position):
        """Verifie si la position est dans la grille"""
        sx,sy=self.taille
        x,y=position
        return (0<=x<sx and 0<=y<sy)

    def est_un_coin(self, position):
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
        """Test la victoire."""
        compteur=cfg.CASE_VIDE
        for colonne in self.grille:
            compteur+=colonne.count(cfg.CASE_VIDE)
        self.gagne=(compteur==cfg.CASE_VIDE)
        return self.gagne



    def getPieces(self,side):
        """Recup toute les position de toues les piece d'un joueur"""
        positions=[]
        sx,sy=self.taille
        for y in range(sy):
            for x in range(sx):
                case = self.obtenir_case((x,y))
                if case==side:
                    positions.append((x,y))
        return positions

    def getAround(self,positions):
        """Prend en parametre une liste de position de case et retourne la liste des postions des cases vide se trouvant juste à cote"""
        environment=[]

        around=[(x,y) for x in range(-1,2) for y in range(-1,2) if (x,y)!=(0,0)]
        for position in positions:
            px,py=position
            for step in around:
                stx,sty=step
                x,y=(px+stx,py+sty)
                if self.est_dans_grille((x,y)):
                    if self.est_une_case_vide((x,y)) :
                        environment.append((x,y))
        return environment

    def inserer_pion(self, coordonnees, side) :
        """inserer_pion insere un pion dans la grille sans se soucier de conquerir le territoire"""
        x,y=coordonnees
        self.grille[y][x]=side

    def reverse_pion(self, coordonnees) :
        """Retourne le pion se trouvant au coordonnees"""
        #Todo pour marc : faire cette foction
        #Utiliser cette methode dans la methode 'conquer'
        pass

    def obtenir_case(self, coordonnees) :
        """Retourn le contenu d'une case"""
        x,y=coordonnees
        return self.grille[y][x]

    def placer_pion(self,coordonnees_pion,side):
        """place un pion sur le plateau"""
        self.inserer_pion(coordonnees_pion, side)
        self.conquerir(coordonnees_pion,side)

    def est_une_case_vide(self, position) :
        return self.obtenir_case(position)==cfg.CASE_VIDE


    def obtenir_mouvements_valides(self,joueur_side,fenetre):
        """Retourne une liste de tuple qui correspondent aux coordonnées des mouvements possibles pour le joueur_side"""
        ennemi_side=1-joueur_side
        positions=self.getPieces(ennemi_side)
        positions=self.getAround(positions)
        mouvements=[]
        for position in positions:
            if self.est_mouvement_valide(position,joueur_side):
                mouvements.append(position)
        return mouvements

    def est_mouvement_valide(self,position,p_side):
        """Permet de verifier si un mouvement est valide"""
        vecteurs=[(x,y) for x in range(-1,2) for y in range(-1,2) if (x,y)!=(0,0)]
        resultat=False
        for vecteur in vecteurs:
            ligne=self.recuperer_ligne(vecteur,position)
            if self.est_mouvement_valide_dans_ligne(p_side,ligne):
                resultat=True
                break
        return resultat

    def est_mouvement_valide_dans_ligne(self,p_side,ligne):
        """Permet de verifier si un mouvement est valide dans une ligne"""
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
            ligne=self.recuperer_ligne(vecteur,position)
            self.conquerir_ligne(p_side,ligne)

    def recuperer_ligne(self,position,vecteur):
        """Recupere la ligne des valeurs obtenue avec une position et un vecteur."""
        line=[]
        vx,vy=vecteur
        x,y=position
        while self.est_dans_grille((x,y)):
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
            self.inserer_pion(mangeable,personne)

    def afficher(self,fenetre):
        self.showGrid(fenetre)
        self.showPieces(fenetre)
        self.showMoves(fenetre)

    def debugMove(self,position,fenetre,couleur):
        #fenetre.clear()
        #self.afficher(fenetre)
        #self.showMove(position,fenetre,couleur)
        #fenetre.flip()
        #fenetre.pause()
        pass

    def showMove(self,move,fenetre,couleur):
        wsx,wsy=fenetre.taille
        sx,sy=self.taille
        radius=int(min(wsx,wsy)/min(sx,sy)/4)
        x,y=move
        raw_position=(int((x+1/2)*wsx/sx),int((y+1/2)*wsy/sy))
        pygame.draw.circle(fenetre.screen,couleur,raw_position,radius,0)

    def showMoves(self,fenetre):
        for move in self.mouvements:
            self.showMove(move,fenetre,self.mouvements_couleur)

    def colorer_case(postion, couleur) :
        """permet de colorer une case du plateau d'une certaine couleur
        cette fonction est utile pour debug de ia.py"""
        pass

    def showGrid(self,fenetre):
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

    def showPieces(self,fenetre):
        """Affiche les pions"""
        wsx,wsy=fenetre.taille
        sx,sy=self.taille
        radius=int(min(wsx,wsy)/min(sx,sy)/2)
        for y in range(sy):
            for x in range(sx):
                case=self.obtenir_case((x,y))
                raw_position=(int((x+1/2)*wsx/sx),int((y+1/2)*wsy/sy))
                if 0<=case and case<=len(self.pieces_couleur)-1 :
                    couleur=self.pieces_couleur[case]
                    pygame.draw.circle(fenetre.screen,couleur,raw_position,radius,0)
