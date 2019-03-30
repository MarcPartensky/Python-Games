from mywindow import Window
from othello import Othello
from player import Robot,Humain
from beast import Beast
#from neuralnetwork import NeuralNetwork

class Simulateur:
    def __init__(self,fenetre,joueurs,nombre_parties=10,affichage=False,display=True):
        self.fenetre=fenetre
        self.nombre_parties=nombre_parties
        self.joueurs=joueurs
        self.affichage=affichage
        self.display=display
        self.gagnants=[]

    def __call__(self):
        for i in range(self.nombre_parties):
            jeu=Othello(self.fenetre,self.joueurs,self.affichage)
            jeu()
            if not jeu.fenetre.open:
                break
            self.gagnants.append(jeu.gagnant)
            if self.display: print(self)

    def __repr__(self):
        message="Resultats de "+str(len(self.gagnants))+" parties:\n"
        for joueur in range(len(self.joueurs)):
            message+="- Joueur "+str(joueur)+" a gagne "+str(self.gagnants.count(joueur))+" fois.\n"
        return message



if __name__=="__main__":
    fenetre=Window(taille=[800,800],fullscreen=False)
    joueurs=[Robot(),Robot()]
    nombre_parties=50
    affichage=True
    simulation=Simulateur(fenetre,joueurs,nombre_parties,affichage)
    simulation()
    print(simulation)
