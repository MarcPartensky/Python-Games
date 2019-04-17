from joueur import Joueur


from config import log
import config as cfg
import couleurs
import outils
import random
import copy

from mywindow import Window


class IA(Joueur):
    def __init__(self):
        """Creer une instance de joueur."""
        self.vitesse_demonstration=0.1
        super().__init__()
        #Vitesse moyenne de démonstration

    def jouer(self,plateau,fenetre):
        """Renvoie le choix du joueur et le sauvegarde en attribut."""
        self.presenterPionsStables(plateau,fenetre)
        choix=self.jouerAleatoire(plateau)
        self.choix=choix
        return choix

    def jouerAleatoire(self,plateau):
        """Joue aleatoirement dans le plateau."""
        mouvements=plateau.obtenirMouvementsValides(self.cote)
        return random.choice(mouvements)

    def presenterPionsStables(self,plateau,fenetre):
        """Presente les pions stables a l'ecran en les trouvant, cela s'effectue a l'aide du plateau et de la fenetre."""
        fenetre.clear()
        plateau.afficher(fenetre)
        tous_les_pions=[]
        for i in range(2):
            pions=self.obtenirTousLesPionsDefinitivementStables(plateau,i,fenetre)
            tous_les_pions.append(pions)
            plateau.presenter(pions,plateau.pieces_couleur[i],fenetre,message="pions stables",pause=False)
            if pions:
                fenetre.attendre(self.vitesse_demonstration)
        log("pions definitivement stables:",tous_les_pions)
        fenetre.clear()
        plateau.afficher(fenetre)
        for i in range(2):
            plateau.presenter(tous_les_pions[i],plateau.pieces_couleur[i],fenetre,message="pions stables",pause=False,clear=False)
        if tous_les_pions.count([])!=2:
            fenetre.attendre() #Par défaut la fenetre attend 1 seconde


    def compterPions(self,plateau,cote=None):
        """Compte les pions de tel couleur, par defaut compte ses propres pions."""
        cote=self.cote
        pions=plateau.obtenirPions(cote)
        return len(pions)

    def obtenirToutesLesLignes(self,plateau):
        """Renvoie la liste de toutes les lignes possibles de la grille."""
        lignes=[]
        tx,ty=plateau.taille
        m=max(plateau.taille)
        for y in range(ty):
            for x in range(tx):
                for direction in plateau.obtenirDirections():
                    for n in range(m):
                        position=(x,y)
                        ligne=plateau.obtenirLigneInclus(position,direction,n)
                        lignes.append(tuple(ligne))
        lignes=list(set(lignes))
        vrai_lignes=[list(ligne) for ligne in lignes]
        return vrai_lignes

    def obtenirToutesLesLignesSansDirection(self,plateau):
        """Renvoie toutes les lignes possibles de la grille mais sans prendre en compte l'ordre des positions de celles-ci."""
        lignes=self.obtenirToutesLesLignes(plateau)
        lignes_triees=[]
        for ligne in lignes:
            ligne.sort()
            lignes_triees.append(tuple(ligne))
        lignes_triees=list(set(lignes_triees))
        lignes=[]
        for ligne_triee in lignes_triees:
            lignes.append(list(ligne_triee))
        return lignes


    def obtenirToutesLesLignesDePions(self,plateau,cote):
        """Renvoie la liste de toutes les lignes de pions de la meme couleur sur le plateau avec le côté du joueur en utilisant par defaut le cote du joueur actif."""
        """Chaque ligne est caractérisée par les pions situés aux extrémités et seules les lignes maximum sont comptées."""
        """Exemple: [((l1x1,l1y1),(l1x2,l1y2)),((l2x1,l2y1),(l2x2,l2y2))] contient les positions de 2 lignes l1 et l2."""
        lignes=[]
        tx,ty=plateau.taille
        for y in range(ty):
            for x in range(tx):
                position=(x,y)
                case=self.obtenirCase(position)
                directions=plateau.obtenirDirections()
                for direction in directions:
                    ligne=plateau.obtenirLigne(direction,position)
                    for position in ligne:
                        if case:
                            pass

    def obtenirLignesVerticales(self,plateau,cote):
        """Renvoie la liste de toutes les lignes verticales du plateau."""
        lignes=[]
        tx,ty=plateau.taille
        for x in range(tx):
            position=(x,0)
            direction=(0,1)
            ligne=plateau.obtenirLigne(direction,position)
            lignes.append(ligne)
        return lignes

    def obtenirCoupsSuivants(self,plateau,choix,cote):
        """Renvoie les coups suivants."""
        nouveau_plateau=copy.deepcopy(plateau)
        nouveau_plateau.placerPion(choix,cote)
        cote_oppose=nouveau_plateau.obtenirCoteOppose(cote)
        mouvements=nouveau_plateau.obtenirMouvementsValides(cote_oppose)
        return mouvements

    def estPionReprenable(self,plateau,pion,cote):
        """Determine si un pion peut être repris juste après pion."""
        nouveau_plateau=copy.deepcopy(plateau)
        nouveau_plateau.placerPion(pion,cote)
        cote_oppose=nouveau_plateau.obtenirCoteOppose(cote)
        mouvements=nouveau_plateau.obtenirMouvementsValides(cote_oppose)
        return bool(pion in mouvements)

    def estSurCoin(self,plateau,pion):
        """Determine si un pion est sur un coin."""
        tx,ty=plateau.taille
        mx,my=tx-1,ty-1
        return bool(pion in [(0,0),(mx,0),(0,my),(mx,my)])

    def estSurBord(self,plateau,pion):
        """Determine si un pion est sur un bord."""
        tx,ty=plateau.taille
        x,y=pion
        return bool((x%(tx-1))*(y%(ty-1))==0)

    def aVoisinSurCoin(self,plateau,pion):
        """Determine si un pion possede un voisin sur coin."""
        resultat=False
        voisins=plateau.obtenirEnvironnement(pion)
        for pion in voisins:
            if self.estSurCoin(plateau,pion):
                resultat=True
                break
        return resultat

    def estDefinitivementStable(self,plateau,pion,fenetre):
        """Determine si un pion est définivement stable en utilisant une approche brute."""
        cote=plateau.obtenirCase(pion)
        lignes=plateau.obtenirLignesAlentours(pion) #lignes de positions
        cote_oppose=plateau.obtenirCoteOppose(cote)
        stable=True
        for (i,ligne) in enumerate(lignes):
            ci=(i+4)%8
            ligne_oppose=lignes[ci] #Permet de récupérer la ligne qui est située a l'opposée de la i-ème ligne.
            cases=plateau.obtenirCases(ligne) #lignes de contenus de cases
            cases_opposees=plateau.obtenirCases(ligne_oppose)
            if cote_oppose in cases:
                if cfg.CASE_VIDE in cases_opposees:
                    stable=False
            if cfg.CASE_VIDE in cases:
                if (cote_oppose in cases_opposees) or (cfg.CASE_VIDE in cases_opposees):
                    stable=False
            plateau.presenter(ligne,couleurs.BLEU,fenetre,message="ligne",pause=False)
            plateau.presenter(ligne_oppose,couleurs.VIOLET,fenetre,message="ligne_oppose",clear=False,pause=False)
            plateau.presenter(pion,couleurs.ROUGE,fenetre,"pion considéré",clear=False,pause=False)
            fenetre.attendre(self.vitesse_demonstration)
            if not stable:
                break
        return stable

    def obtenirTousLesPionsDefinitivementStables(self,plateau,cote,fenetre):
        """Renvoie la liste de tous les pions qui sont definitivement stables."""
        stables=[]
        pions=plateau.obtenirPions(cote)
        #plateau.presenter(pions,couleurs.ROUGE,fenetre,"pions"+str(cote))
        for pion in pions:
            if self.estDefinitivementStable(plateau,pion,fenetre):
                stables.append(pion)
        return stables

    def estDefinitivementStable3(self,plateau,pion):
        environnement=self.environnementStableTrival(plateau,pion)
        validite=self.estEnvironnementValide(environnement)
        if validite:
            return True
        else:
            pass



    def estEnvironnementValide(self,environnement,n):
        environnement_double=environnement+environnement
        valide=False
        c=0
        for stable in double_environnement:
            if stable:
                c+=1
                if c>n:
                    valide=True
                    break
            else:
                c=0
        return valide



    def environnementStableComplet(self,plateau,pion):
        pass


    def environnementStableTrivial(self,plateau,pion):
        directions=plateau.obtenirDirections()
        environnement=[]
        for direction in directions:
            dx,dy=direction
            px,py=pion
            position=(px+dx,py+dy)
            if not plateau.estDansGrille(position):
                environnement.append(True)
            else:
                environnement.append(None)




    def obseleteEstPionDefinitivementStable2(self,plateau,pion):
        """Determine si un pion est définitivement stable."""
        if self.estSurCoin(plateau,pion):
            return True
        else:
            directions=plateau.obtenirDirections()
            arrangements=outils.arrangementsConsecutifs(directions)
            for arrangement in arrangements:
                for position in arrangement:
                    ligne=plateau.obtenirLigne(direction,pion)
                    pass


    def obseleteEstPionDefinitivementStable(self,plateau,pion):
        """Determine si un pion est assuré i.e. si un pion est définitevement
        posé et ne pourra être repris plus tard dans la partie."""
        directions=plateau.obtenirDirections()
        for i in range(len(directions)):
            cinq_directions=directions[i,i]
            definitivement_stable=True
            for direction in cinq_directions:
                ligne=plateau.obtenirLigne(direction,pion)
                if cfg.CASE_VIDE in ligne:
                    definitivement_stable=False
                    break
            if definitevement_stable:
                return True


    def estPionStable(self,plateau,pion):
        """Determine si un pion stable."""
        #Implémenter la stabilité d'Alexandre
        if not self.estPrenable(pion):
            stable=True
        else:
            pass


    def estPrenable(self,plateau,pion):
        """Determine si un pion est prenable a l'instant."""
        cote=plateau.obtenirCase(pion)
        cote_ppose=plateau.obtenirCoteOppose(cote)
        mouvements=plateau.obtenirMouvementsValides(cote)
        return bool(pion in mouvements)

    def obtenirPionsStables(self,plateau,cote):
        """Renvoie la liste de tous les pions stables sur le plateau appartenant au joueur du côté 'cote'."""
        pions=plateau.obtenirPions(cote)
        pions_stables=[]
        for pion in pions:
            if self.estPionStable(pion):
                pions_stables.append(pion)
        return pions

    def estLigneStable(self,plateau,position):
        """Determine si une ligne est stable."""
        pass #Ajouter la définition de la stabilité d'Alexandre

    def obtenirCarres(self,plateau,cote):
        """Renvoie l'ensemble des carrés de pions dans le plateau qui appartiennent au joueur du côté 'cote'."""
        pass #A compléter

    def obtenirTriangles(self,plateau,cote):
        """Renvoie la liste des triangles de pions dans le plateau qui appartiennent au joueur du côté 'cote'."""
        pass #A compléter
