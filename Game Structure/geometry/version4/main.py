from mypoint import Point
from myform import Form
from myvector import Vector
from mywindow import Window
from mysurface import Surface
from mycolors import RED,WHITE

from random import randint

"""This is a demonstration of the potential of the project, it shows the easiness
to make complex interactions between defined forms using only few lines of codes."""
#window=Window()

window=Surface()
#The trick is to use the surface as a window since the behavious are mainly alike
#Indeed the surface was designed to answer all the needs of the clients as if it
#was a window but is in reality a completely different type using somekind of
#kernel pattern using only a true window as a attribute and being a intermediary.
#This intermediary is necessary in order to change the coordonnate system of the window.
#It is pivotal that all the coordonnates involved in future programs remain in plane's
#coordonnates' system for simplicity.
wsx,wsy=window.draw.window.size
X=wsx//4
Y=wsy//4

#posAlea=lambda :[randint(X,3*X),randint(Y,3*Y)] #Obsolete
#posAlea=lambda:(randint(-5,5),randint(-5,5))


#f1=Form([Point(*posAlea()) for i in range(5)],fill=True) #Obsolete
#f1=f1.getSparse()
f1=Form.random(5,-10,10)
#f2=Form([Point(*posAlea()) for i in range(5)])
#f2=f2.getSparse()
f2=Form.random(5,-10,10)

#f1.points[0].color=(255,0,0)
#f1.points[1].color=(255,0,0)

while window.open:
    window.check()
    window.clear()
    window.show()
    window.control()
    f1.rotate(0.01,f1[0])
    #f1.rotate(-0.01)
    f2.rotate(0.02,f1[1])
    f2.rotate(-0.03)
    f1.show(window)
    f2.show(window)
    f1.center(color=(0,255,0)).show(window)
    f2.center(color=(0,255,0)).show(window)
    if f1|f2:
        f1.color(RED)
        f2.color(RED)
    else:
        f1.color(WHITE)
        f2.color(WHITE)
    f1[0].show(window,color=(255,0,0))
    f1[1].show(window,(255,0,0))

    window.flip()
