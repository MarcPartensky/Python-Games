from joueur import Joueur

from couleurs import *
from config import log
import config as cfg
import outils
import random
import copy

from mywindow import Window


class IA(Joueur):
    def __init__(self):
        """Creer une instance de joueur."""
        super().__init__()

    def jouer(self,plateau,fenetre):
        """Joue."""
        pions=self.obtenirTousLesPionsDefinitivementStables(plateau,self.cote,fenetre)
        for pion in pions:
            plateau.colorerCase(pion,(255,255,0),fenetre)
        choix=self.jouerAleatoire(plateau)
        log("pions definitivement stables:",pions)
        self.choix=choix
        return choix

    def jouerAleatoire(self,plateau):
        """Joue aleatoirement dans le plateau."""
        mouvements=plateau.obtenirMouvementsValides(self.cote)
        return random.choice(mouvements)

    def compterPions(self,plateau,cote=None):
        """Compte les pions de tel couleur, par defaut compte ses propres pions."""
        cote=self.cote
        pions=plateau.obtenirPions(cote)
        return len(pions)

    def obtenirLignes(self,plateau,cote):
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
        """Determine si un pion est définitement stable."""
        cote=plateau.obtenirCase(pion)
        environnement=plateau.obtenirAlentours(pion)
        log("environnement:",environnement)
        plateau.afficher(fenetre)
        plateau.afficherMessage("pion:",pion,NOIR,fenetre)
        plateau.colorerCase(pion,BLEU,fenetre)
        plateau.afficherMessage("environnement:",environnement[0],NOIR,fenetre)
        plateau.colorerCase(environnement,ORANGE,fenetre)
        fenetre.flip()
        fenetre.pause()
        log("pion:",pion)
        log("environnement:",environnement)
        stable=True
        for position in environnement:
            vecteur=outils.vecteur(pion,position)
            log("vecteur:",vecteur)
            ligne=plateau.obtenirLigneExclus(pion,vecteur)
            log("ia:ligne:",ligne)
            plateau.afficherMessage("ia:ligne:",ligne[0],NOIR,fenetre)
            plateau.colorerCase(ligne,ROSE,fenetre)
            fenetre.flip()
            fenetre.pause()
            if not outils.estRemplie(ligne,cote):
                stable=False
                break
        log("stable:",stable)
        return stable

    def obtenirTousLesPionsDefinitivementStables(self,plateau,cote,fenetre):
        """Renvoie la liste de tous les pions qui sont definitivement stables."""
        stables=[]
        pions=plateau.obtenirPions(cote)
        log("pions:",pions)
        plateau.afficherMessage("pions",pions[0],NOIR,fenetre)
        plateau.colorerCase(pions,ROUGE,fenetre)
        fenetre.flip()
        fenetre.pause()
        for pion in pions:
            if self.estDefinitivementStable(plateau,pion,fenetre):
                stables.append(pion)
        if stables:
            plateau.afficherMessage("stables",stables[0],NOIR,fenetre)
            plateau.colorerCase(stables,VIOLET,fenetre)
            fenetre.flip()
            fenetre.pause()
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
