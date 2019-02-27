class Entity:
    made=0
    def __init__(self,name="Unnamed",id=None,position=None,size=None,colliding_box=None,spawn_position=None,velocity=[0,0],acceleration=[0,0]):
        """Create entity object using name, id, position, size, colliding_box, spawn_position, velocity and acceleration."""
        Entity.made+=1
        self.number=Entity.made
        self.name=name
        self.id=id
        self.position=position
        self.size=size
        self.spawn_position=spawn_position
        self.velocity=velocity
        self.acceleration=acceleration
        self.load()

    def load(self):
        """Load specific entity attributs."""
        self.alive=False
        self.mass=None
        self.gravitional_constant=9.81

    def move(self):
        """Move entity."""
        for i in range(self.dimensions):
            self.velocity[i]+=self.acceleration[i]
            self.position[i]+=self.velocity[i]

    def getNextPosition(self):
        ax,ay=self.acceleration
        vx,vy=self.velocity
        x,y=self.position
        vx+=ax
        vy+=ay
        x+=vx
        y+=vy
        return (x,y)

    def spawn(self):
        self.alive=True
        if self.spawn_position is not None:
            self.position=self.spawn_position

    def die(self):
        self.alive=False

    def show(self,window):
        pass

    def collide(self,entity):
        if self.colliding_box is not None and entity.colliding_box is not None:
            x,y=self.getNextPosition()
            ex,ey=entity.getNextPosition()
            bx,by=self.colliding_box
            ebx
