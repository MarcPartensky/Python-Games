from mywindow_regression import Window
from curve import Curve

fenetre=Window("Regression test",size=[1440,900],fullscreen=True)

while fenetre.open:
    #fenetre.points=[]
    fenetre.draw()
    courbe=Curve(fenetre.points)
    #courbe.linearRegression(fenetre.points)
    fenetre.clear()
    courbe.show(fenetre)
    fenetre.flip()
#cout=courbe.cost(courbe.coefficients)
fenetre.pause()
print(courbe.cout)
