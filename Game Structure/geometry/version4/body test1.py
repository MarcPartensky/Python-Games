from mysurface import Surface
from mybody import Body
from myabstract import Form,Point,Vector
from mymotion import Motion

import mycolors

surface=Surface()


dt=1

form=Form([Point(0,1),Point(0,0),Point(1,0),Point(1,1)],area_color=mycolors.BLUE,fill=True)
#form=Circle(copy.deepcopy(Point.origin()),radius=1,fill=True,color=mycolors.BLUE)
body=Body(form)
missile=None

def createRandomBody():
    form=5*Form.random(n=5)
    form.side_color=mycolors.RED
    form.area_color=mycolors.BLACK
    form.fill=True
    motion=Motion(10*Vector.random(),Vector.random(),Vector.null())
    moment=Motion(Vector([1]),Vector([0.1]))
    return Body(form,motion,moment)

n=10
bodies=[createRandomBody() for i in range(n)]



while surface.open:
    #Surface
    surface.check()
    #surface.control()
    surface.clear()
    surface.show()
    surface.controlZoom()

    #Control
    body.control(surface,v=0.1)
    new_missile=body.shoot(surface)
    if new_missile is not None:
        missile=new_missile

    #Update
    for i in range(len(bodies)):
        #bodies[i].motion.velocity=copy.deepcopy(-bodies[i].motion.position/1000)
        bodies[i].follow(body.position)
        bodies[i].update(dt)
    body.update(dt)
    if missile is not None:
        missile.update(dt)


    if missile:
        for i in range(len(bodies)):
            p=bodies[i].absolute.crossSegment(missile.absolute)
            print(p)
            if len(p)>0:
                bodies[i]=createRandomBody()



    #Show
    for body_ in bodies:
        body_.absolute.showAll(surface)
    body.show(surface)
    if missile is not None:
        missile.show(surface)
        missile.absolute.p2.show(surface,color=mycolors.ORANGE)


    surface.draw.plane.position=copy.deepcopy(body.position)
    if missile is not None:
        surface.draw.window.print(str(missile.velocity),(10,10),20)

    surface.flip()
