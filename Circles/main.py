from mylab import Lab
from circle import Circle
from random import randint as rdt

from math import sqrt,atan,cos,sin

class Room(Lab):
    def __init__(self,name="Room",circles_number=5):
        self.name=name
        self.factor=1
        Lab.__init__(self,name)
        self.window.size=[1440,900]
        self.window.fullscreen=True
        self.window.text_size=20
        self.window.set()
        wsx,wsy=self.window.size
        v=3
        self.entities=[Circle(position=[rdt(0,wsx),rdt(0,wsy)],velocity=[rdt(-v,v),rdt(-v,v)],acceleration=[0,0],mass=rdt(1,100),borders=[[0,wsx],[0,wsy]]) for i in range(circles_number)]

    def update(self):
        self.affectCollisions()
        for entity in self.entities:
            entity.update()
        self.affectFriction()

    def affectFriction(self):
        f=self.factor
        for entity in self.entities:
            entity.velocity=[f*entity.velocity[0],f*entity.velocity[1]]


    def affectCollisions(self):
        l=len(self.entities)
        for y in range(l):
            for x in range(y):
                self.affectCollision(self.entities[y],self.entities[x])


    def affectCollision(self,entity1,entity2):
        x1,y1=entity1.position
        x2,y2=entity2.position
        r1=entity1.radius
        r2=entity2.radius
        if sqrt((x1-x2)**2+(y1-y2)**2)<r1+r2:
            self.affectVelocity(entity1,entity2)


    def affectVelocity(self,entity1,entity2):
        x1,y1=entity1.position
        x2,y2=entity2.position
        vx1,vy1=entity1.velocity
        vx2,vy2=entity2.velocity
        m1=entity1.mass
        m2=entity2.mass
        if x2!=x1:
            angle=-atan((y2-y1)/(x2-x1))
            ux1,uy1=self.rotate(entity1.velocity,angle)
            ux2,uy2=self.rotate(entity2.velocity,angle)
            v1=[self.affectOneVelocity(ux1,ux2,m1,m2),uy1]
            v2=[self.affectOneVelocity(ux2,ux1,m1,m2),uy2]
            entity1.velocity=self.rotate(v1,-angle)
            entity2.velocity=self.rotate(v2,-angle)

    def affectOneVelocity(self,v1,v2,m1,m2):
        return (m1-m2)/(m1+m2)*v1+(2*m2)/(m1+m2)*v2

    def rotate(self,velocity,angle):
        vx,vy=velocity
        nvx=vx*cos(angle)-vy*sin(angle)
        nvy=vx*sin(angle)+vy*cos(angle)
        return [nvx,nvy]






if __name__=="__main__":
    room=Room("Vive les cercles",10)
    room()
