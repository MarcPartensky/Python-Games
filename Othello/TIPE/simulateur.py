from mywindow import Window
from othello import Othello
from jouer import Robot,Humain
from bruteforce import BruteForce
from ia import IA
#from neuralnetwork import NeuralNetwork

class Simulateur:
    def __init__(self,joueurs,nombre_parties=10,fenetre=None):
        """Cree un simulateur de partie avec une fenetre, des joueurs, un nombre de partie"""
        self.fenetre=fenetre
        self.nombre_parties=nombre_parties
        self.joueurs=joueurs
        self.affichage=affichage
        self.display=display
        self.gagnants=[]

    def __call__(self):
        """Boucle 'for' principale du simulateur."""
        for i in range(self.nombre_parties):
            if self.fenetre:
                jeu=Othello(self.joueurs,self.fenetre)
            else:
                jeu=Othello(self.joueurs)
            jeu()
            if not jeu.fenetre.open:
                break
            self.gagnants.append(jeu.gagnant)
            if self.display: print(self)

    def __repr__(self):
        """Renvoie une représentation des victoires de chaque joueur avec l'historice des victoires du simulateur."""
        message="Resultats de "+str(len(self.gagnants))+" parties:\n"
        for numeror in range(len(self.joueurs)):
            message+="- Joueur "+str(numero)+" a gagne "+str(self.gagnants.count(numero))+" fois.\n"
        return message



if __name__=="__main__":
    fenetre=Window(taille=[800,800],fullscreen=False)
    joueurs=[IA(),BruteForce(3)]
    nombre_parties=50
    affichage=True
    simulation=Simulateur(fenetre,joueurs,nombre_parties)
    simulation()
    print(simulation)
