from plateau import Plateau
from config import log

import config as cfg
import outils
import couleurs
import copy

class PlateauAnalysable(Plateau):

    def __init__(self,*args,**kwargs):
        """Creer un plateau analysable."""
        self.vitesse_demonstration=0.1 #Possibilité de changer la vitesse de démonstration
        self.pions_definitivement_stables=None
        self.pions_stables=None
        super().__init__(*args,**kwargs)

    def chargerAnalyse(self,fenetre):
        """Charge l'ensemble des ses attributs d'analyse pour les ias qui s'en servent."""
        pions0_definitivement_stables=self.obtenirTousLesPionsDefinitivementStables(0,fenetre)
        pions1_definitivement_stables=self.obtenirTousLesPionsDefinitivementStables(1,fenetre)
        self.pions_definitivement_stables=[pions0_definitivement_stables,pions1_definitivement_stables]
        pions0_prenables=self.obtenirTousLesPionsPrenables(0,fenetre)
        pions1_prenables=self.obtenirTousLesPionsPrenables(1,fenetre)
        self.pions_prenables=[pions0_prenables,pions1_prenables]
        pions0_stables=self.obtenirTousLesPionsStables(0,fenetre)
        pions1_stables=self.obtenirTousLesPionsStables(1,fenetre)
        self.pions_stables=[pions0_stables,pions1_stables]
        #Un petit peu de présentation pour faire joli
        for i in range(2):
            self.presenter(self.pions_stables[i],self.pieces_couleur[i],fenetre,"stables")
            self.presenter(self.pions_prenables[i],self.pieces_couleur[i],fenetre,"prenables")
            self.presenter(self.pions_definitivement_stables[i],self.pieces_couleur[i],fenetre,"definitivement_stables",clear=False,pause=False)
            fenetre.attendre(0.5)

    def obtenirToutesLesLignes(self):
        """Renvoie la liste de toutes les lignes possibles de la grille."""
        lignes=[]
        tx,ty=self.taille
        m=max(self.taille)
        for y in range(ty):
            for x in range(tx):
                for direction in self.obtenirDirections():
                    for n in range(m):
                        position=(x,y)
                        ligne=self.obtenirLigneInclus(position,direction,n)
                        lignes.append(tuple(ligne))
        lignes=list(set(lignes))
        vrai_lignes=[list(ligne) for ligne in lignes]
        return vrai_lignes


    def obtenirToutesLesLignesSansDirection(self):
        """Renvoie toutes les lignes possibles de la grille mais sans prendre en compte l'ordre des positions de celles-ci."""
        lignes=self.obtenirToutesLesLignes()
        lignes_triees=[]
        for ligne in lignes:
            ligne.sort()
            lignes_triees.append(tuple(ligne))
        lignes_triees=list(set(lignes_triees))
        lignes=[]
        for ligne_triee in lignes_triees:
            lignes.append(list(ligne_triee))
        return lignes

    def presenterPionsStables(self,fenetre): #Obselète
        """Presente les pions stables a l'ecran en les trouvant, cela s'effectue avec la fenetre."""
        fenetre.clear()
        self.afficher(fenetre)
        tous_les_pions=[]
        for i in range(2):
            pions=self.obtenirTousLesPionsDefinitivementStables(i,fenetre)
            tous_les_pions.append(pions)
            self.presenter(pions,self.pieces_couleur[i],fenetre,message="pions stables",pause=False)
            if pions:
                fenetre.attendre(self.vitesse_demonstration)
        log("pions definitivement stables:",tous_les_pions)
        fenetre.clear()
        plateau.afficher(fenetre)
        for i in range(2):
            plateau.presenter(tous_les_pions[i],self.pieces_couleur[i],fenetre,message="pions stables",pause=False,clear=False)
        if tous_les_pions.count([])!=2:
            fenetre.attendre() #Par défaut la fenetre attend 1 seconde


    def obtenirTousLesPionsDefinitivementStables(self,cote,fenetre):
        """Renvoie la liste de tous les pions qui sont definitivement stables."""
        stables=[]
        pions=self.obtenirPions(cote)
        #plateau.presenter(pions,couleurs.ROUGE,fenetre,"pions"+str(cote))
        for pion in pions:
            if self.estUnPionDefinitivementStable(pion,fenetre):
                stables.append(pion)
        return stables

    def estUnPionDefinitivementStable(self,pion,fenetre):
        """Determine si un pion est définivement stable en déterminant pour chaque ligne auquel il appartient, si il peut être définitivement stable.
        Pour cela, on se ramène à un problème plus simple: c'est à dire vérifier la stabilité d'un pion dans une ligne.
        Ainsi on vérifie pour chaque ligne auquelle ce pion appartient, si celui-ci peut-être définitivment stable, et si c'est bien le cas,
        alors ce pion est définitivment stable sans équivoque."""
        cote=self.obtenirCase(pion)
        lignes=self.obtenirLignesAlentours(pion) #lignes de positions
        cote_oppose=self.obtenirCoteOppose(cote)
        stable=True
        for (i,ligne) in enumerate(lignes):
            ci=(i+4)%8
            ligne_oppose=lignes[ci] #Permet de récupérer la ligne qui est située a l'opposée de la i-ème ligne.
            cases=self.obtenirCases(ligne) #lignes de contenus de cases
            cases_opposees=self.obtenirCases(ligne_oppose)
            if cote_oppose in cases:
                if cfg.CASE_VIDE in cases_opposees:
                    stable=False
            if cfg.CASE_VIDE in cases:
                if (cote_oppose in cases_opposees) or (cfg.CASE_VIDE in cases_opposees):
                    stable=False
            """Présentation des lignes sur l'écran pour le mode démonstration."""
            self.presenter(ligne,couleurs.BLEU,fenetre,message="ligne",pause=False)
            self.presenter(ligne_oppose,couleurs.VIOLET,fenetre,message="ligne_oppose",clear=False,pause=False)
            self.presenter(pion,couleurs.ROUGE,fenetre,"pion considéré",clear=False,pause=False)
            fenetre.attendre(self.vitesse_demonstration)
            if not stable:
                break
        return stable

    def obtenirTousLesPionsStables(self,cote,fenetre):
        """Renvoie la liste de tous les pions stables sur le plateau appartenant au joueur du côté 'cote'."""
        pions=self.obtenirPions(cote)
        pions_stables=[]
        for pion in pions:
            if self.estUnPionStable(pion,fenetre):
                pions_stables.append(pion)
        return pions

    def estUnPionStable(self,pion,fenetre,niveau=1): #Cette fonction est toujours pas fonctionnelle
        """Détermine si un pion est stable."""
        cote=self.obtenirCase(pion) #Obtient le cote du joueur ayant pose le pion
        cote_oppose=self.obtenirCoteOppose(cote) #Recupere le cote oppose avec le cote du joueur
        mouvements=self.obtenirMouvementsValides(cote_oppose) #recupere tous les mouvements enemis
        #Determine si un pion est imprenable
        if not self.estUnPionPrenable(pion): #Si c'est le cas, il est stable
            stable=True #On sauve le fait que le pion soit stable
        else: #Sinon lorsqu'il est prenable, il est stable uniquement si celui-ci devient instable apres etre pris
            stable=True #On suppose au départ le pion stable, et on cherche un mouvement qui perment de discréditer cette supposition
            for mouvement in mouvements: #Fait une itération de chaque mouvement un par un
                nouveau_plateau=copy.deepcopy(self) #On copie le plateau pour simuler chaque mouvement enemi
                nouveau_plateau.placerPion(mouvement,cote_oppose) #On joue le mouvement enemi itéré dans le nouveau plateau
                nouveau_cote=nouveau_plateau.obtenirCase(pion) #On récupère la couleur du pion après le mouvement enemi
                if nouveau_cote!=cote: #Détermine si ce pion est pris i.e. la couleur de ce pion dans le nouveau plateau,est différente de celle d'avant
                    nouveau_plateau.afficher(fenetre) #Réaffiche pour le debug
                    nouveau_plateau.presenter(pion,couleurs.ORANGE,fenetre,"niveau:"+str(niveau),couleur_texte=couleurs.ORANGE) #Affiche le pion que l'on considère et le niveau de récusion
                    if nouveau_plateau.estUnPionStable(pion,fenetre,niveau+1): #Détermine si ce pion devient stable après être pris
                        stable=False #Si c'est le cas alors forcément il n'est pas devenu instable donc le pion ne pouvait pas être stable à la base
                        break #Donc comme ce pion ne peut pas être stable, il n'y a pas de raison de vérifier s'il peut l'être pour d'autre mouvements
        return stable #On renvoie le booléen correspondant à la stabilité du pion

    def obtenirTousLesPionsPrenables(self,cote,fenetre):
        """Renvoie la liste de tous les pions d'un côté 'cote' qui sont prenables au tour suivant."""
        pions=self.obtenirPions(cote)
        prenables=[]
        for pion in pions:
            if self.estUnPionPrenable(pion):
                prenables.append(pion)
        return prenables

    def estUnPionPrenable(self,pion):
        """Determine si un pion est prenable a l'instant en utilisant le pion."""
        cote=self.obtenirCase(pion)
        cote_oppose=self.obtenirCoteOppose(cote)
        mouvements=self.obtenirMouvementsValides(cote_oppose)
        prenable=False
        for mouvement in mouvements:
            nouveau_plateau=copy.deepcopy(self)
            nouveau_plateau.placerPion(mouvement,cote_oppose)
            nouveau_cote=nouveau_plateau.obtenirCase(pion)
            if nouveau_cote!=cote:
                prenable=True
                break
        return prenable



    def estLigneDefinitivementStable(self,ligne):
        """Determine si une ligne est stable."""
        ligne=outils.obtenirLigneComplete(ligne)
        stable=True
        for pion in ligne:
            if not pion in self.pions_stables:
                stable=False
                break
        return stable

    def obtenirCarres(self,cote):
        """Renvoie l'ensemble des carrés de pions dans le plateau qui appartiennent au joueur du côté 'cote'."""
        pass #A compléter

    def obtenirTriangles(self,cote):
        """Renvoie la liste des triangles de pions dans le plateau qui appartiennent au joueur du côté 'cote'."""
        pass #A compléter
