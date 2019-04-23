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
        self.vitesse_demonstration=0.1 #Possibilité de changer la vitesse de démonstration
        super().__init__()


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

    def compterPions(self,plateau,cote=None):
        """Compte les pions de tel couleur, par defaut compte ses propres pions."""
        cote=self.cote
        pions=plateau.obtenirPions(cote)
        return len(pions)

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
