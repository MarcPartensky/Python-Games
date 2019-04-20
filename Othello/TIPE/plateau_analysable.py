from plateau import Plateau
from config import log

import config as cfg
import outils
import couleurs

class PlateauAnalysable(Plateau):

    def __init__(self,*args,**kwargs):
        """Creer un plateau analysable."""
        self.vitesse_demonstration=0.1 #Possibilité de changer la vitesse de démonstration
        super().__init__(*args,**kwargs)

    def chargerAnalyse(self,fenetre):
        """Charge l'ensemble des ses attributs d'analyse pour les ias qui s'en servent."""
        self.pions0_stables=self.obtenirTousLesPionsDefinitivementStables(0,fenetre)
        self.pions1_stables=self.obtenirTousLesPionsDefinitivementStables(1,fenetre)
        self.pions_stables=self.pions0_stables+self.pions1_stables

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

    def presenterPionsStables(self,fenetre): #A voir
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
            if self.estDefinitivementStable(pion,fenetre):
                stables.append(pion)
        return stables

    def estDefinitivementStable(self,pion,fenetre):
        """Determine si un pion est définivement stable en déterminant pour chaque ligne auquel il appartient, si il peut être définitivement stable."""
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
            self.presenter(ligne,couleurs.BLEU,fenetre,message="ligne",pause=False)
            self.presenter(ligne_oppose,couleurs.VIOLET,fenetre,message="ligne_oppose",clear=False,pause=False)
            self.presenter(pion,couleurs.ROUGE,fenetre,"pion considéré",clear=False,pause=False)
            fenetre.attendre(self.vitesse_demonstration)
            if not stable:
                break
        return stable

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
