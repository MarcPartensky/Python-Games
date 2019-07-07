from myabstract import Form,Vector,Point,Segment,Circle
from mymotion import Motion
from mymaterial import Material

from pygame.locals import *
import logging
import copy
import mycolors

class Body(Material):
    def createFromAbsolute(form,motion=Motion(),moment=Motion(d=1)):
        """Create a body from an absolute form."""
        motion.position=Vector(*form.center)
        print(motion.position)
        form.points=(-motion.position).applyToPoints(form.points)
        return Body(form,motion,moment)

    def __init__(self,form,motion=Motion(d=2),moment=Motion(d=1)):
        """Create body using form and optional name."""
        self.form=form
        self.motion=motion
        self.moment=moment

    def __str__(self):
        """Return the string representation of the body."""
        return "b("+str(self.form)+","+str(self.motion)+")"

    def show(self,context):
        """Show the form on the window."""
        self.absolute.show(context)

    def update(self,dt=1):
        """Move entity according to its acceleration, velocity and position."""
        self.motion.update(dt)
        self.moment.update(dt)

    def control(self,context,v=1):
        """Raw control the view of the plane."""
        #logging.warning("This function should not be used in big project because events must be treated it the main loop and only once.")
        """keys=context.press()
        if keys[K_DOWN]:
            self.motion.velocity[1]=-v
        if keys[K_UP]:
            self.motion.velocity[1]=v
        if keys[K_LEFT]:
            self.motion.velocity[0]=-v
        if keys[K_RIGHT]:
            self.motion.velocity[0]=v"""
        self.follow(context.point(),1/10)



    def shoot(self,context):
        """Return a missile."""
        #logging.warning("This function is only a test and should not be included in the body class but in a child class instead.""")
        keys=context.press()
        p=Point(*context.point())
        if keys[K_SPACE]:
            k=0.1
            c=Point(*self.position)
            v=Vector.createFromTwoPoints(c,p)
            v.norm=1
            m=Motion(copy.deepcopy(self.position),v+copy.deepcopy(self.velocity),Vector.null())
            o=Point.origin()
            s=Segment(o,v(o))
            b=Body(s,m)
            return b
        else:
            return None

    def getAbsolute(self):
        """Return a copy of the form in absolute coordonnates."""
        p=Point(*tuple(copy.deepcopy(self.position)))
        f=copy.deepcopy(self.form)
        f.center=p
        f.rotate(self.moment.position[0])
        return f

    def setAbsolute(self,form):
        """Set the form of the body using the absolute form."""
        self.position=Vector(*form.center)
        p=Point(*tuple(copy.deepcopy(-self.position)))
        form.center=p
        self.form=form


    def __contains__(self,point):
        """Determine if a point is in the body."""
        return point in self.absolute

    def follow(self,point,speed=1/100):
        """Update the motion in order for a body to follow a given point."""
        v=Vector(*point)
        self.velocity=(v-self.position)/10
        if self.velocity.norm>1:
            self.velocity.norm=1





    absolute=property(getAbsolute,setAbsolute)



if __name__=="__main__":
    from mysurface import Surface
    surface=Surface(fullscreen=True)

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
