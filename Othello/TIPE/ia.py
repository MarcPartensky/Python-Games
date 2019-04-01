from copy import deepcopy
import random
import player
from outils import intersection
from outils import est_superieur
from outils import deco_debug
import outils
import config as cfg

ZONE_COIN=4#Ne doit pas etre une liste
ZONE_BORD=3
ZONE_BLANCHE=2
ZONE_ROUGE=1
ZONE_NOIR=0
ZONE_TOUT=-1


LISTE_ZONES=[ZONE_COIN,ZONE_BORD,ZONE_BLANCHE,ZONE_ROUGE,ZONE_NOIR, ZONE_TOUT]

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
            if PLATEAU_COLORE[x][y]==key or key==ZONE_TOUT :
                result.append((x,y))
    LISTE_POSITION_ZONE[key]=result


class IA(player.Robot) :
    def __init__(self):
       pass


    def reinitialiser(self, plateau):
        self.plateau=plateau#il ne faut surtout pas faire des simulations sur ce plateau !!
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
            if self.obtenir_couleur_position(position)==zone :
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
        return PLATEAU_COLORE[position[0]][position[1]]

    def testSiJoueurSidePossedeUneDeCesPositions(self, plateau, side, positions):
        """Prend une liste de positions dans le plateau est verifi si le joueur de side
        side possede un pion a l'une des position de la liste"""
        resultat=False
        for position in positions:
            if plateau.estCaseJoueur(position, side):
                resultat=True
                break
        return resultat

    def testSiJoueurSidePossedeTouesCesPositions(self, plateau, side, positions):
        """Prend une liste de positions dans le plateau est verifi si le joueur de side
        side possede tout les pions sur les position de la liste"""
        for position in positions:
            if not(plateau.estCaseJoueur(position, side)):
                return False
        return True

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
                postions=[positions]

        mouvements_possible_side=plateau.obtenirMouvementsValides(side)

        for position_posible_joueur_side in mouvements_possible_side :
            plateau_simulation=deepcopy(self.plateau)
            plateau_simulation.placerPion(position_posible_joueur_side, side)

            if self.testSiJoueurSidePossedeUneDeCesPositions(positions, side) :#on verif si le  coup à permit de prendre une des positions
                resultat=True
                break
        return resultat


    def test_peut_etre_repris_tout_suite_apres(self, position):
        """on considere que position est une case valide du plateau est que c'est un mouv possible"""
        plateau_simulation=deepcopy(self.plateau)
        plateau_simulation.placerPion(position, self.side)
        side_adversaire=plateau_simulation.obtenir_side_joueur_oppose(self.side)
        return self.test_si_le_joueur_side_peut_prendre_position(plateau_simulation, side_adversaire, position)

    def obtenirLesPositionsDansZone(self, positions, zone):#Todo, utiliser les fonctions build-in de python
        """Renvoie une liste des positions de positions se trouvant dans la zone zone"""
        resultat=[]
        for position in positions :
            if self.obtenir_couleur_position(position)==zone:
                resultat.append(position)
        return resultat

    def est_coup_bourbier_par_cote(self, plateau, pos, cote):
        """Dertermine si le coup à la positions pos joue par le joueur cote emepche l'adv de jouer au prochain tour"""
        cote_oppose=1-cote
        plateau_simulation = deepcopy(plateau)
        plateau_simulation.placerPion(pos, cote)
        return len(plateau_simulation.obtenirMouvementsValides(cote_oppose)) <= 0

    def obtenir_coups_bourbier(self, plateau, cote):
        coup_bourbier=[]
        MouvementsValides=plateau.obtenirMouvementsValides(cote)
        for mouvement in MouvementsValides :
            if self.est_coup_bourbier_par_cote(plateau, mouvement, cote) :
                coup_bourbier.append(mouvement)
        return coup_bourbier

    def obtenirPositionAleatoireDansZone(self, positions, zone):
        """On considere qu'on a au moins une coup possible dans la zone en question"""
        return random.choice(self.obtenirLesPositionsDansZone(positions, zone))

    def Nombre_pion_retourne(self, plateau, pos):
        """"Renvoie le nombre de pion qui sont retourne lorsque self pose un pion à la position pos sur le plateau plateau."""
        plateau_simulation = deepcopy(plateau)
        nombre_init=plateau_simulation.obtenirNombrePionsJoueur(pos)
        plateau_simulation.placerPion(pos, self.side)
        nombre_final=plateau_simulation.obtenirNombrePionsJoueur(pos)
        return nombre_final-nombre_init-1#-1 car on pose un pion

    #@deco_debug
    def Augmentation_coup_possible_adv_dans_zone(self, plateau, pos, zone):
        """"Renvoie de combien augmente le nombe de coup possible de l'adversaire dans la zone zone apres que self ait joué à pos"""
        plateau_simulation = deepcopy(plateau)
        coup_possible_dans_zone=intersection(outils.liste_liste_vers_liste_tuple(plateau_simulation.obtenirMouvementsValides(self.cote_oppose)), LISTE_POSITION_ZONE[zone])
        nombre_coup_possible_dans_zone=len(coup_possible_dans_zone)
        plateau_simulation.placerPion(pos, self.cote)
        final_coup_possible_dans_zone=intersection(outils.liste_liste_vers_liste_tuple(plateau_simulation.obtenirMouvementsValides(self.cote_oppose)), LISTE_POSITION_ZONE[zone])
        final_nombre_coup_possible_dans_zone=len(final_coup_possible_dans_zone)
        return final_nombre_coup_possible_dans_zone-nombre_coup_possible_dans_zone

    @deco_debug
    def Nombre_pion_stable_zone(self, plateau, cote, zone):
        resultat=0
        #cfg.debug("qw:",plateau.obtenirPions(cote))
        #cfg.debug("wq:",LISTE_POSITION_ZONE[zone])
        position_pion_zone=intersection(outils.liste_liste_vers_liste_tuple(plateau.obtenirPions(cote)), LISTE_POSITION_ZONE[zone])
        for pos in position_pion_zone :
            if self.est_stable_pour_cote(plateau, [pos], cote) :
                resultat+=1
        return resultat

    @deco_debug
    def Augmentation_pion_stable_dans_zone(self, plateau, cote, zone, pos):
        """"Renvoie de combien augmente le nombe de pion stable de cote dans la zone zone apres que cote ait joué à pos"""
        plateau_simulation = deepcopy(plateau)
        nombre_initial=self.Nombre_pion_stable_zone(plateau, cote, zone)
        plateau_simulation.placerPion(pos, cote)
        nombre_final = self.Nombre_pion_stable_zone(plateau, cote, zone)
        return nombre_final-nombre_initial

    def Augmentation_pion_dans_zone(self, plateau, cote, zone, pos):
        """"Renvore de cb on augmente le nombre de pion de cote dans la zone zone apres que cote joue à pos"""
        plateau_simulation = deepcopy(plateau)
        nombre_initial=len(outils.intersection(outils.liste_liste_vers_liste_tuple(plateau_simulation.obtenirPions(cote)), LISTE_POSITION_ZONE[zone]))
        plateau_simulation.placerPion(pos, cote)
        nombre_final = len(outils.intersection(outils.liste_liste_vers_liste_tuple(plateau_simulation.obtenirPions(cote)), LISTE_POSITION_ZONE[zone]))
        return nombre_final-nombre_initial

    def Nombre_coin_adjacent_pris(self, plateau, cote, pos_coin):#todo debug ?
        resultat=0
        x,y=pos_coin
        #size=len(PLATEAU_COLORE)#==7
        if plateau.estCaseJoueur(((x+7)%14, y), cote) :
            resultat+=1
        if plateau.estCaseJoueur((x, (y+7)%14), cote) :
            resultat+=1
        return resultat

    #@deco_debug
    def est_stable_pour_cote(self, plateau, liste_de_position, cote):#todo debug cette fonction
        #plateau_simulation = deepcopy(plateau)


        #cfg.debug("###on lance est_stable_pour_cote")
        cote_oppose=1-cote
        liste_des_cas_particuliers={}
        mouv_valide_adv=plateau.obtenirMouvementsValides(cote_oppose)
        for mouv in mouv_valide_adv :
            plateau_simulation = deepcopy(plateau)
            plateau_simulation.placerPion(mouv, cote_oppose)
            #if self.testSiJoueurSidePossedeUneDeCesPositions(plateau_simulation, cote_oppose, liste_de_position):
            if self.testSiJoueurSidePossedeTouesCesPositions(plateau_simulation, cote_oppose, liste_de_position):
                #On est dans le deuxième cas
                #cfg.debug("liste_des_cas_particuliers1 :", liste_des_cas_particuliers)
                #cfg.debug("le mouv associ1:", mouv)
                #cfg.debug("le plateau:", plateau_simulation)
                liste_des_cas_particuliers[tuple(mouv)]=plateau_simulation#verif que plateau simul est pas ecraser à la prochaine iteration
                #cfg.debug("liste_des_cas_particuliers2 :", liste_des_cas_particuliers)

        if liste_des_cas_particuliers=={}:
            #L'adv ne peut pas prendre les positions quelque soit ses mouvement
            return True
        else :
            for mouv_cas_particulier in liste_des_cas_particuliers:
                #la liste est alors stable si pour tout les mouv, liste_de_position+[mouv_cas_particulier] est instable pour cote oppose
                nouvelle_ligne=liste_de_position+[mouv_cas_particulier]
                plateau_de_ce_cas=liste_des_cas_particuliers[mouv_cas_particulier]
                if self.est_stable_pour_cote(plateau_de_ce_cas, nouvelle_ligne, cote_oppose) :
                    #l'adv a reussi a former une ligne stable, cela signifie la ligne de depart etait instable
                    return False
            #L'adv ne peut pas former une ligne stable en prenant notre ligne, notre ligne est donc stable
            return True

    @deco_debug
    def position_stable_pour_cote(self, plateau, position,cote):
        plateau_simulation = deepcopy(plateau)
        plateau_simulation.placerPion(position, cote)
        return self.est_stable_pour_cote(plateau_simulation, [position], cote)

    @deco_debug
    def comparer_blanc(self, pos1, pos2):
        coeff1,coeff2=[],[]
        coeff1.append(self.Nombre_pion_retourne(self.plateau, pos1))
        coeff2.append(self.Nombre_pion_retourne(self.plateau, pos2))
        outils.ajouter_coeff_alea(coeff1, coeff2)
        if est_superieur(coeff1, coeff2) :
            return pos1
        else :
            return pos2

    @deco_debug
    def comparer_rouge(self, pos1, pos2):
        coeff1,coeff2=[],[]
        coeff1.append(-1*self.Augmentation_coup_possible_adv_dans_zone(self.plateau, pos1, ZONE_BORD))
        coeff2.append(-1*self.Augmentation_coup_possible_adv_dans_zone(self.plateau, pos2, ZONE_BORD))
        coeff1.append(self.Nombre_pion_retourne(self.plateau, pos1))
        coeff2.append(self.Nombre_pion_retourne(self.plateau, pos2))
        outils.ajouter_coeff_alea(coeff1, coeff2)
        if est_superieur(coeff1, coeff2) :
            return pos1
        else :
            return pos2

    @deco_debug
    def comparer_vert(self, pos1, pos2):
        coeff1,coeff2=[],[]

        coeff1.append(self.Augmentation_pion_stable_dans_zone(self.plateau, self.cote, ZONE_BORD, pos1))
        coeff2.append(self.Augmentation_pion_stable_dans_zone(self.plateau, self.cote, ZONE_BORD, pos2))

        coeff1.append(self.Augmentation_pion_dans_zone(self.plateau, self.cote, ZONE_BORD, pos1))
        coeff2.append(self.Augmentation_pion_dans_zone(self.plateau, self.cote, ZONE_BORD, pos2))

        coeff1.append(self.Nombre_pion_retourne(self.plateau, pos1))
        coeff2.append(self.Nombre_pion_retourne(self.plateau, pos2))

        outils.ajouter_coeff_alea(coeff1, coeff2)
        if est_superieur(coeff1, coeff2) :
            return pos1
        else :
            return pos2

    @deco_debug
    def comparer_noir(self, pos1, pos2):
        coeff1,coeff2=[],[]

        coeff1.append(-1*self.Augmentation_coup_possible_adv_dans_zone(self.plateau, pos1, ZONE_COIN))
        coeff1.append(-1*self.Augmentation_coup_possible_adv_dans_zone(self.plateau, pos2, ZONE_COIN))

        coeff1.append(int(self.position_stable_pour_cote(self.plateau, pos1, self.cote)))
        coeff2.append(int(self.position_stable_pour_cote(self.plateau, pos2, self.cote)))

        #todo faire cas Case noir sur l'extrême bord, juste à côté d’un coin conquis

        coeff1.append(self.Nombre_pion_retourne(self.plateau, pos1))
        coeff2.append(self.Nombre_pion_retourne(self.plateau, pos2))

        outils.ajouter_coeff_alea(coeff1, coeff2)
        if est_superieur(coeff1, coeff2) :#todo utiliser le mot cle or en python
            return pos1
        else :
            return pos2

    def comparer_coin(self, pos1, pos2):
        coeff1,coeff2=[],[]

        coeff1.append(self.Nombre_coin_adjacent_pris(self.plateau, self.cote, pos1))
        coeff2.append(self.Nombre_coin_adjacent_pris(self.plateau, self.cote, pos2))

        coeff1.append(self.Augmentation_pion_stable_dans_zone(self.plateau, self.cote, ZONE_BORD, pos1))
        coeff2.append(self.Augmentation_pion_stable_dans_zone(self.plateau, self.cote, ZONE_BORD, pos2))

        coeff1.append(self.Augmentation_pion_dans_zone(self.plateau, self.cote, ZONE_BORD, pos1))
        coeff2.append(self.Augmentation_pion_dans_zone(self.plateau, self.cote, ZONE_BORD, pos2))

        coeff1.append(self.Nombre_pion_retourne(self.plateau, pos1))
        coeff2.append(self.Nombre_pion_retourne(self.plateau, pos2))

        outils.ajouter_coeff_alea(coeff1, coeff2)
        if est_superieur(coeff1, coeff2) :
            return pos1
        else :
            return pos2

    @deco_debug
    def comparer_blanc_rouge(self, blanc, rouge):

        if self.Augmentation_coup_possible_adv_dans_zone(self.plateau, rouge, ZONE_BORD)<=0:
            if self.Nombre_pion_retourne(self.plateau, rouge)>=self.Nombre_pion_retourne(self.plateau, blanc) :
                return rouge
        return blanc

    @deco_debug
    def comparer_blanc_vert(self, blanc, vert):#todo faire un debug affichable
        if self.position_stable_pour_cote(self.plateau, blanc, self.cote) :
            if not(self.position_stable_pour_cote(self.plateau, vert, self.cote)) :
                if self.Nombre_pion_retourne(self.plateau, blanc)>=self.Nombre_pion_retourne(self.plateau, vert) :
                    cfg.debug("##Cas particulier {} est mieux que {}")
                    return blanc
        return vert

    @deco_debug
    def comparer_blanc_noir(self, blanc, noir):#todo faire un debug affichable
        if self.Augmentation_coup_possible_adv_dans_zone(self.plateau, noir, ZONE_COIN)<=0:
            #Ok on peut envisager de jouer noir
            coeff_blanc, coeff_noir=[],[]
            coeff_blanc.append(self.Augmentation_pion_stable_dans_zone(self.plateau, self.cote, ZONE_TOUT, blanc))
            coeff_noir.append(self.Augmentation_pion_stable_dans_zone(self.plateau, self.cote, ZONE_TOUT, noir))

            coeff_blanc.append(self.Nombre_pion_retourne(self.plateau, blanc))
            coeff_noir.append(self.Nombre_pion_retourne(self.plateau, noir))

            outils.ajouter_coeff_alea(coeff_blanc, coeff_noir)

            cfg.debug("##Cas particu noir {} est mieux que blanc {}".format(noir, blanc))
            if est_superieur(coeff_blanc, coeff_noir):
                return blanc
            else:
                return noir


        return blanc

    @deco_debug
    def comparer_blanc_coin(self, blanc, coin):
        return coin

    @deco_debug
    def comparer_rouge_vert(self, rouge, vert):#todo revoir ca + debug affichage
        if not(self.position_stable_pour_cote(self.plateau, vert, self.cote)) :
            if self.position_stable_pour_cote(self.plateau, rouge, self.cote) :
                cfg.debug("##Cas particulier, le rouge {} est mieux que le vert {}".format(rouge, vert))
                return rouge
        return vert

    @deco_debug
    def comparer_rouge_noir(self, rouge, noir):#todo revoir ca + debug affichage
        if self.Augmentation_coup_possible_adv_dans_zone(self.plateau, noir, ZONE_COIN)<=0:
            #Ok on peut envisager de jouer noir
            coeff_rouge, coeff_noir = [], []

            coeff_rouge.append(self.Augmentation_pion_stable_dans_zone(self.plateau, self.cote, ZONE_TOUT, rouge))
            coeff_noir.append(self.Augmentation_pion_stable_dans_zone(self.plateau, self.cote, ZONE_TOUT, noir))

            coeff_rouge.append(self.Nombre_pion_retourne(self.plateau, rouge))
            coeff_noir.append(self.Nombre_pion_retourne(self.plateau, noir))

            outils.ajouter_coeff_alea(coeff_rouge, coeff_noir)
            if est_superieur(coeff_rouge, coeff_noir):
                return rouge
            else:
                return noir

        return rouge

    @deco_debug
    def comparer_rouge_coin(self, rouge, coin):
        return coin

    @deco_debug
    def comparer_vert_noir(self, vert, noir):
        if self.Augmentation_coup_possible_adv_dans_zone(self.plateau, noir, ZONE_COIN)<=0:
            #Ok on peut envisager de jouer noir
            coeff_vert, coeff_noir = [], []

            coeff_vert.append(self.Augmentation_pion_stable_dans_zone(self.plateau, self.cote, ZONE_BORD, vert))
            coeff_noir.append(self.Augmentation_pion_stable_dans_zone(self.plateau, self.cote, ZONE_BORD, noir))

            coeff_vert.append(self.Augmentation_pion_dans_zone(self.plateau, self.cote, ZONE_BORD, vert))
            coeff_noir.append(self.Augmentation_pion_dans_zone(self.plateau, self.cote, ZONE_BORD, noir))

            coeff_vert.append(self.Nombre_pion_retourne(self.plateau, vert))
            coeff_noir.append(self.Nombre_pion_retourne(self.plateau, noir))

            outils.ajouter_coeff_alea(coeff_vert, coeff_noir)
            if est_superieur(coeff_vert, coeff_noir):
                return vert
            else:
                return noir


        return vert

    @deco_debug
    def comparer_vert_coin(self, vert, coin):
        return coin

    @deco_debug
    def comparer_noir_coin(self, noir, coin):
        return coin

    def comparer(self, position1, position2):
        liste_degueulasse={ZONE_BLANCHE:{ZONE_BLANCHE:self.comparer_blanc,
                                         ZONE_ROUGE:self.comparer_blanc_rouge,
                                         ZONE_BORD:self.comparer_blanc_vert,
                                         ZONE_NOIR:self.comparer_blanc_noir,
                                         ZONE_COIN:self.comparer_blanc_coin},

                           ZONE_ROUGE:{  ZONE_ROUGE:self.comparer_rouge,
                                         ZONE_BORD:self.comparer_rouge_vert,
                                         ZONE_NOIR:self.comparer_rouge_noir,
                                         ZONE_COIN:self.comparer_rouge_coin},

                           ZONE_BORD:{   ZONE_BORD:self.comparer_vert,
                                         ZONE_COIN:self.comparer_vert_coin,
                                         ZONE_NOIR:self.comparer_vert_noir},
                           ZONE_NOIR:{ZONE_NOIR:self.comparer_noir,
                                      ZONE_COIN:self.comparer_noir_coin},
                           ZONE_COIN:{ZONE_COIN:self.comparer_coin}


                           }
        try :
            fonction_compa=liste_degueulasse[self.obtenir_couleur_position(position1)][self.obtenir_couleur_position(position2)]
            arg=(position1, position2)
        except KeyError :
            fonction_compa = liste_degueulasse[self.obtenir_couleur_position(position2)][self.obtenir_couleur_position(position1)]
            arg = (position2, position1)

        if self.Augmentation_coup_possible_adv_dans_zone(self.plateau, arg[0], ZONE_COIN) <= 0:
            if self.Augmentation_coup_possible_adv_dans_zone(self.plateau, arg[1], ZONE_COIN) <= 0:
                return fonction_compa(arg[0], arg[1])
            else :
                return arg[0]
        else :
            if self.Augmentation_coup_possible_adv_dans_zone(self.plateau, arg[1], ZONE_COIN) <= 0:
                return arg[1]
            else :
                return fonction_compa(arg[0], arg[1])


    def compa_diago(self, fct2,*args):
        if len(args) == 1:
            return args[0]
        elif len(args) == 2:
            return fct2(args[0], args[1])
        #cfg.debug("le args", args)
        return self.compa_diago(fct2,fct2(args[0], args[1]), *args[2:])

    def main(self, plateau):
        self.reinitialiser(plateau)  # Il faut prednre en compte le nouveau plateau
        coups_bourbier=self.obtenir_coups_bourbier(self.plateau, self.cote)
        if coups_bourbier!=[] :
            cfg.debug("##Coup Bourbier !")
            return self.compa_diago(self.comparer, *coups_bourbier)
        else :
            return self.compa_diago(self.comparer, *self.mouvements_possibles)


    """
    def main(self, plateau_objet) :
        #if not(self.test_acces_zone(self, ZONE_BORD)):
        self.reinitialiser(plateau_objet)#Il faut prednre en compte le nouveau plateau

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
"""
