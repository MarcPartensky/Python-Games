from copy import deepcopy
import random
import player
from outils import intersection

ZONE_COIN=4#Ne doit pas etre une liste
ZONE_BORD=3
ZONE_BLANCHE=2
ZONE_ROUGE=1
ZONE_NOIR=0

LISTE_ZONES=[ZONE_COIN,ZONE_BORD,ZONE_BLANCHE,ZONE_ROUGE,ZONE_NOIR]

PLATEAU_COLORE=[[ZONE_COIN, ZONE_NOIR ,ZONE_BORD   ,ZONE_BORD   ,ZONE_BORD   ,ZONE_BORD   ,ZONE_NOIR ,ZONE_COIN],
                [ZONE_NOIR, ZONE_NOIR ,ZONE_ROUGE  ,ZONE_ROUGE  ,ZONE_ROUGE  ,ZONE_ROUGE  ,ZONE_NOIR ,ZONE_NOIR],
                [ZONE_BORD, ZONE_ROUGE,ZONE_BLANCHE,ZONE_BLANCHE,ZONE_BLANCHE,ZONE_BLANCHE,ZONE_ROUGE,ZONE_BORD],
                [ZONE_BORD, ZONE_ROUGE,ZONE_BLANCHE,ZONE_BLANCHE,ZONE_BLANCHE,ZONE_BLANCHE,ZONE_ROUGE,ZONE_BORD],
                [ZONE_BORD, ZONE_ROUGE,ZONE_BLANCHE,ZONE_BLANCHE,ZONE_BLANCHE,ZONE_BLANCHE,ZONE_ROUGE,ZONE_BORD],
                [ZONE_BORD, ZONE_ROUGE,ZONE_BLANCHE,ZONE_BLANCHE,ZONE_BLANCHE,ZONE_BLANCHE,ZONE_ROUGE,ZONE_BORD],
                [ZONE_NOIR, ZONE_NOIR ,ZONE_ROUGE  ,ZONE_ROUGE  ,ZONE_ROUGE  ,ZONE_ROUGE  ,ZONE_NOIR ,ZONE_NOIR],
                [ZONE_COIN, ZONE_NOIR ,ZONE_BORD   ,ZONE_BORD   ,ZONE_BORD   ,ZONE_BORD   ,ZONE_NOIR ,ZONE_COIN]]

LISTE_POSITION_ZONE={}
for i in range(len(LISTE_ZONES)):#Permet de generer LISTE_POSITION_ZONE
    result=[]
    key=LISTE_ZONES[i]
    for x in range(len(PLATEAU_COLORE)) :
        for y in range(len(PLATEAU_COLORE[x])):
            if PLATEAU_COLORE[x][y]==key :
                result.append((x,y))
    LISTE_POSITION_ZONE[key]=result



class IA(player.Robot) :
    def __init__(self, plateau, side):
        self.plateau=plateau#il ne faut surtout pas faire des simulations sur ce plateau !!
        self.side=side
        self.mouvements_possibles=plateau.obtenirMouvementsValides(self.side)

    def testToutPionsDansZones(self, plateau, zones):
        """Test si tout les pions du plateau sont dans les zones zones"""
        if not isinstance(zones,list):
            zones=[zones]
        resultat=True
        positions=plateau.obtenirPositionsPions()
        for position in positions:
            if not(self.obtenir_couleur_position(position) in zones) :
                resultat=False
                break
        return resultat


    def test_acces_zone(self, zone) :
        resultat=False
        for position in self.mouvements_possibles:
            if obtenir_couleur_position(position)==zone :
                resultat=True
                break
        return resultat

    def obtenir_couleur_position(self, position):
        #"""Retourne si coin, zone blanche etc..."""
        a="""positions_bord=[(1,0),(self.plateau.taille_x-2,0),
                        (0,1),(1,1),(self.plateau.taille_x-2,1), (self.plateau.taille_x-1,1),
                        (0,self.plateau.taille_y-2),(1,self.plateau.taille_y-2), (self.plateau.taille_x-2,self.plateau.taille_y-2),(self.plateau.taille_x-1,self.plateau.taille_y-2),
                        (1,self.plateau.taille_y-1),(self.plateau.taille_x-2,self.plateau.taille_y-1)
                        ]
        """
        return PLATEAU_COLORE[postion[0]][postion[1]]

    def testSiJoueurSidePossedeUneDeCesPositions(self, plateau, side, positions):
        """Prend une liste de positions dans le plateau est verifi si le joueur de side
        side possede un pion a l'une des position de la liste"""
        resultat=False
        for position in postions:
            if plateau.est_une_case_joueur_side(position, side):
                resultat=True
                break
        return resultat

    def test_si_le_joueur_side_peut_prendre_position(self,plateau, side, positions):
        """on considere que position est une case valide du plateau
        On a un plateau, c'est le tour de joueur side est on souhaite determiner, si dans ses mouvements possibles,
        un permet d'avoir une pion de sa couleur dans une des position de la liste positiones dans le plateau

        positions peut etre une liste ou simple coo (si )
        """

        resultat=False

        if isinstance(positions, tuple) :
            if len(positions)==2 :
                #positions n'est pas une liste de positions mais jsute une couplde coo:
                postions=[postions]

        mouvements_possible_side=plateau.obtenirMouvementsValides(side)

        for position_posible_joueur_side in mouvements_possible_side :
            plateau_simulation=deepcopy(self.plateau)
            plateau_simulation.placer_pion(position_posible_joueur_side, side)

            if self.testSiJoueurSidePossedeUneDeCesPositions(positions, side) :#on verif si le  coup à permit de prendre une des positions
                resultat=True
                break
        return resultat


    def test_peut_etre_repris_tout_suite_apres(self, position):
        """on considere que position est une case valide du plateau est que c'est un mouv possible"""
        plateau_simulation=deepcopy(self.plateau)
        plateau_simulation.placer_pion(position, self.side)
        side_adversaire=plateau_simulation.obtenir_side_joueur_oppose(self.side)
        return self.test_si_le_joueur_side_peut_prendre_position(plateau_simulation, side_adversaire, position)

    def obtenirLesPositionsDansZone(self, positions, zone):#Todo, utiliser les fonctions build-in de python
        """Renvoie une liste des positions de positions se trouvant dans la zone zone"""
        resultat=[]
        for position in positions :
            if self.obtenir_couleur_position(position)==zone:
                resultat.append(position)
        return resultat

    def test_placement_permet_adversaire_jouer_position(plateau, position_placement, postion_case):#todo
        #A terminer
        plateau_simulation=deepcopy(plateau)
        pass


    def obtenirPositionAleatoireDansZone(self, positions, zone):
        """On considere qu'on a au moins une coup possible dans la zone en question"""
        return random.choice(self.obtenirLesPositionsDansZone(positions, zone))


    def main(self) :
        #if not(self.test_acces_zone(self, ZONE_BORD)):
        if self.testToutPionsDansZones(self.plateau, ZONE_BLANCHE) :#alors tout les pions sont dans la zone blanche c'est necore le debut de la particulier
            return self.obtenirPositionAleatoireDansZone(self.mouvements_possibles, ZONE_BLANCHE)
            #Si c'est le debut du jeu, alors on joue aleatoirement dans ZONE_BLANCHE
        #Sinon on essai de jouer dans
        #QUand on joue sur les bords on ne veut pas etre repris juste après
        if intersection(LISTE_POSITION_ZONE[ZONE_BORD], self.mouvements_possibles)!=[]:
            coups_interressant_sur_bord=[]#ensemble coup possible sur le bords ou on n'est pas pirs juste apres
            for position in intersection(LISTE_POSITION_ZONE[ZONE_BORD], self.mouvements_possibles):
                if not self.test_peut_etre_repris_tout_suite_apres(position) :
                    coups_interressant_sur_bord.append(position)
            if coups_interressant_sur_bord :#si coups_interressant_sur_bord est pas vide
                return random.choice(coups_interressant_sur_bord)




def main(plateau_objet,side):
    """fonction obligatoire dans ia.py"""


###################
    def prioriter_coup_possible(self):
        """ renvoie le meilleur coup possible par ordre de priorité des couleurs """
        coups_possible = obtenirMouvementsValides(side)

        for cp in coups_possible :
            if obtenir_couleur_position(cp) >= obtenir_couleur_position(position):
                position = cp
        return position
