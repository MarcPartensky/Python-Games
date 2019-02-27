from math import cos,sin,exp
from cmath import polar,rect

class Entity:
    made=0
    def __init__(self,name="Unnamed",id=None,position=None,size=None,velocity=[0,0],acceleration=[0,0],borders=None,direction=[0,0],friction=0,dimensions=2,moving_function=lambda x:200*x,controllable=False):
        """Create entity object using name, id, position, size, velocity and acceleration."""
        Entity.made+=1
        self.made=Entity.made
        self.name=name
        self.id=id
        self.position=position
        self.size=size
        self.velocity=velocity
        self.acceleration=acceleration
        self.borders=borders
        self.direction=direction #relative to [0,0] in polar coordonnate
        self.friction=friction
        self.dimensions=dimensions
        self.controllable=controllable
        self.moving_function=moving_function

    def move(self):
        """Move entity."""
        for i in range(self.dimensions):
            self.velocity[i]+=self.acceleration[i]
            self.position[i]+=self.velocity[i]

    def affectFriction(self):
        """Affect friction on velocity."""
        self.velocity=[self.velocity[i]*(1-self.friction) for i in range(self.dimensions)]

    def affectBorders(self):
        """Correct borders crossing."""
        x,y=self.position
        sx,sy=self.size
        bx,by,bsx,bsy=self.borders
        if x<0: x=0
        if x+sx>=bsx: x=bsx-sx-1
        if y<0: y=0
        if y+sy>=bsy: y=bsy-sy-1
        self.position=[x,y]

    def detectBorder(self):
        """Detect borders crosssing."""
        x,y=self.position
        sx,sy=self.size
        bx,by,bsx,bsy=self.borders
        if x<bx: return True
        if x+sx>=bx+bsx: return True
        if y<by: return True
        if y+sy>by+bsy: return True
        return False

    def polar(self,position):
        """Return polar position using cartesian position."""
        return list(polar(complex(position[0],position[1])))

    def cartesian(self,position):
        """Return cartesian position using polar position."""
        return [position[0]*cos(position[1]),position[0]*sin(position[1])]


    def old_follow(self):
        """Lead entity towards its direction."""
        vx,vy=self.velocity
        a,n=self.direction
        #print(vx,vy)
        vx+=n*cos(a)
        vy+=n*sin(a)
        #print(n*cos(a),n*sin(a))
        self.velocity=[vx,vy]

    def follow(self):
        """Follow its direction."""
        vx,vy=self.velocity
        r,a=self.polar(self.direction)
        r=self.moving_function(r)
        #print(r,a)
        vx+=r*cos(a)
        vy+=r*sin(a)
        self.velocity=[vx,vy]

    def direct(self,window):
        """Update direction using window."""
        wsx,wsy=window.size
        wpx,wpy=window.point()
        x,y=self.position
        sx,sy=self.size
        self.direction=[((wpx-wsx//2)-(x-sx//2))/wsx,((wpy-wsy//2)-(y-sy//2))/wsy]

    def update(self,window):
        """Update entity's position."""
        if self.controllable: self.direct(window)
        self.follow()
        self.affectFriction()
        self.move()
        self.affectBorders()



if __name__=="__main__":
    e=Entity()
    print(e)
