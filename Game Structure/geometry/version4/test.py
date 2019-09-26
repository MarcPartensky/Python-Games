from myabstract import Form,Segment,Line,Vector,Point

from mysurface import Surface
surface=Surface(name="Test")

#line=Line.random()
#segment=Segment.random()
#print(line|segment)

import mycolors
import math

vector=Vector(1,0)
point=Point(0,0)


while surface.open:
    surface.check()
    surface.control()
    surface.clear()
    surface.show()
    vector.rotate(0.1)
    a=vector.angle
    wl=mycolors.bijection(a,[-math.pi,math.pi],[380,780])
    c=mycolors.setFromWavelength(wl)
    vector.show(surface,point,color=c)
    surface.console("angle: ",str(a),nmax=20)
    #surface.print('something',(10,10),size=100,conversion=False)
    surface.flip()
