ZONE_COIN=0
ZONE_BORD=1
ZONE_ROUGE=2
ZONE_MORT=3
ZONE_BLANCHE=4

PLATEAU_COLORE=[[ZONE_COIN,ZONE_MORT, ZONE_BORD, ZONE_BORD, ZONE_BORD, ZONE_BORD,ZONE_MORT, ZONE_COIN],
                [ZONE_MORT,ZONE_MORT,ZONE_ROUGE,ZONE_ROUGE,ZONE_ROUGE,ZONE_ROUGE,ZONE_MORT,ZONE_MORT],
                [ ZONE_BORD,ZONE_ROUGE, ZONE_BLANCHE, ZONE_BLANCHE, ZONE_BLANCHE, ZONE_BLANCHE,ZONE_ROUGE, ZONE_BORD],
                [ ZONE_BORD,ZONE_ROUGE, ZONE_BLANCHE, ZONE_BLANCHE, ZONE_BLANCHE, ZONE_BLANCHE,ZONE_ROUGE, ZONE_BORD],
                [ ZONE_BORD,ZONE_ROUGE, ZONE_BLANCHE, ZONE_BLANCHE, ZONE_BLANCHE, ZONE_BLANCHE,ZONE_ROUGE, ZONE_BORD],
                [ ZONE_BORD,ZONE_ROUGE, ZONE_BLANCHE, ZONE_BLANCHE, ZONE_BLANCHE, ZONE_BLANCHE,ZONE_ROUGE, ZONE_BORD],
                [ZONE_MORT,ZONE_MORT,ZONE_ROUGE,ZONE_ROUGE,ZONE_ROUGE,ZONE_ROUGE,ZONE_MORT,ZONE_MORT],
                [ ZONE_COIN,ZONE_MORT, ZONE_BORD, ZONE_BORD, ZONE_BORD, ZONE_BORD,ZONE_MORT, ZONE_COIN]]


class IA() :
    def __init__(self, plateau):
        self.plateau=plateau

    def obtenir_couleur_position(position):
        #"""Retourne si coin, zone blanche etc..."""

        positions_bord=[(1,0),(self.plateau.taille_x-2,0),
                        (0,1),(1,1),(self.plateau.taille_x-2,1), (self.plateau.taille_x-1,1),
                        (0,self.plateau.taille_y-2),(1,self.plateau.taille_y-2), (self.plateau.taille_x-2,self.plateau.taille_y-2),(self.plateau.taille_x-1,self.plateau.taille_y-2),
                        (1,self.plateau.taille_y-1),(self.plateau.taille_x-2,self.plateau.taille_y-1)
                        ]
        return PLATEAU_COLORE[postion[0]][postion[1]]




def main(plateau_objet):
    """fonction obligatoire dans ia.py"""
