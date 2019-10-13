from myabstract import Form,Vector,Point,Segment
from mybody import Body
from mymotion import Motion
from mysurface import Context
from pygame.locals import *

import socket
import itertools
import mycolors
import random
import copy
import time

class AsteroidGame:
    def createRandomBody(self):
        """Create a random body."""
        form=5*Form.random(n=5)
        form.side_color=mycolors.RED
        form.area_color=mycolors.BLACK
        form.fill=True
        motion=Motion(10*Vector.random(),Vector.random(),Vector.null())
        moment=Motion(Vector([1]),Vector([0.1]))
        return Body(form,motion,moment)

    def random(self,mi,ma,n):
        """Return a list random terms of size n."""
        return [random.uniform(mi,ma) for i in range(n)]

    def showInfo(self):
        """Show informations about the bodies on the game."""
        if self.missile is not None:
            self.context.draw.window.print(str(self.missile.velocity),(10,10),20)

class SoloAsteroid(AsteroidGame):
    """Asteroid game in solo without connection."""
    def __init__(self,context,dt=0.5):
        """Create a game."""
        self.context=context
        self.dt=dt
        self.asteroids=[Asteroid(self.random(-10,10,2)) for i in range(10)]
        self.spaceships=[Spaceship(Vector(0,100))]
        self.missiles=[]

    def main(self):
        """Main loop."""
        while self.context.open:
            self.show()
            self.events()
            self.update()


    def events(self):
        """Deal with the events."""
        keys=self.context.press()
        p=Point(*self.context.point())
        v=Vector(*(p-Point(*self.spaceships[0].position)))/10
        self.spaceships[0].velocity=v
        self.context.draw.plane.position=copy.deepcopy(self.spaceships[0].position.components)
        missile=self.spaceships[0].shoot(self.context)
        if missile is not None:
            self.missiles.append(missile)



    def show(self):
        """Show the components on the screen."""
        self.context.check()
        self.context.controlZoom()
        self.context.clear()
        self.context.show()
        self.showBodies()
        self.showInfo()
        self.context.flip()

    def showBodies(self):
        """Show all the bodies of the game."""
        self.showSpaceships()
        self.showMissiles()
        self.showAsteroids()

    def showSpaceships(self):
        """Show all the spaceships on the context."""
        for i in range(len(self.spaceships)):
            self.spaceships[i].absolute.show(self.context)

    def showMissiles(self):
        """Show all the missiles on the context."""
        for i in range(len(self.missiles)):
            self.missiles[i].absolute.show(self.context)

    def showAsteroids(self):
        """Show all the asteroids on the context."""
        for i in range(len(self.asteroids)):
            self.asteroids[i].absolute.show(self.context)

    def showInfo(self):
        """Show infos about the game."""
        pass

    def update(self):
        """Update the bodies."""
        self.updateAsteroids()
        self.updateSpaceships()
        self.updateMissiles()
        self.handleCollision()
        if len(self.spaceships)==0:
            self.spaceships.append(Spaceship(Vector(0,100)))


    def updateAsteroids(self):
        """Update all the asteroids."""
        for i in range(len(self.asteroids)):
            self.asteroids[i].update(self.dt)

    def updateSpaceships(self):
        """Update all the spaceships."""
        for i in range(len(self.spaceships)):
            self.spaceships[i].update(self.dt)

    def updateMissiles(self):
        """Update all the missiles."""
        alives=[]
        for i in range(len(self.missiles)):
            self.missiles[i].update(self.dt)
            alives.append(self.missiles[i].alive)
        self.missiles=list(itertools.compress(self.missiles,alives))

    def handleCollision(self):
        """Handle collisions between the missiles and the bodies."""
        self.spaceships,self.missiles=  self.handleGroupCollisions(self.spaceships,self.missiles)
        self.spaceships,self.asteroids= self.handleGroupCollisions(self.spaceships,self.asteroids)
        self.asteroids,self.missiles=   self.handleGroupCollisions(self.asteroids,self.missiles)

    def handleGroupCollisions(self,group1,group2):
        """Handle collisions between the players and the missiles."""
        l1=len(group1)
        l2=len(group2)
        indices1=[1 for i in range(l1)]
        indices2=[1 for i in range(l2)]
        for i in range(l1):
            for j in range(l2):
                ps=group1[i].absolute|group2[j].absolute
                c=int(len(ps)==0)
                indices1[i]=c
                indices2[j]=c
        group1=list(itertools.compress(group1,indices1))
        group2=list(itertools.compress(group2,indices2))
        return (group1,group2)

class Asteroid(Body):
    """Asteroid of the game of Asteroid."""
    def __init__(self,position,size=5):
        """Create an asteroid."""
        form=size*Form.random(n=5)
        form.side_color=mycolors.RED
        form.area_color=mycolors.DARKGREY
        form.fill=True
        motion=Motion(Vector(*position),Vector.random(),Vector.null())
        moment=Motion(Vector([0]),Vector([random.uniform(-1,1)]))
        super().__init__(form,motion,moment)


class Missile(Body):
    def __init__(self,form,position,velocity,max_duration=3):
        """Create body using form and optional name."""
        motion=Motion(position,velocity)
        moment=Motion.null(n=1,d=1)
        super().__init__(form,motion,moment)
        self.to=time.time()
        self.alive=True
        self.max_duration=max_duration

    def update(self,dt=1):
        """Move entity according to its acceleration, velocity and position."""
        self.motion.update(dt)
        self.moment.update(dt)
        if time.time()-self.to>=self.max_duration:
            self.alive=False

    def __str__(self):
        return "Missile("+str(self.position)+","+str(self.velocity)+")"



class Spaceship(Body):
    def __init__(self,position):
        """Create body using form and optional name."""
        form=Form([Point(x,y) for (x,y) in [(0,1),(-1,-1),(1,-1)]])
        motion=Motion(position,Vector.null(d=2),Vector.null(d=2))
        moment=Motion.null(d=1,n=2)
        super().__init__(form,motion,moment)

    def shoot(self,context):
        """Return a missile."""
        #logging.warning("This function is only a test and should not be included in the body class but in a child class instead.""")
        keys=context.press()
        point=Point(*context.point())
        if keys[K_SPACE]:
            center=Point(*self.position)
            direction=Vector.createFromTwoPoints(center,point)
            direction.norm=2
            origin=Point.origin()
            form=Segment(origin,direction(origin))
            position=copy.deepcopy(self.position+direction(origin))
            velocity=direction+copy.deepcopy(self.velocity)
            return Missile(form,position,velocity)


if __name__=="__main__":
    context=Context()
    game=SoloAsteroid(context,dt=0.5)
    game.main()
    print("The solo game is done running.")
