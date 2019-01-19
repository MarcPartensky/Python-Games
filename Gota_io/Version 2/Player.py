class Player:
    def __init__(self,name=None,skin=None):
        self.name=name
        self.skin=skin
        self.color=random.choice(COLORS)
        self.speed_constant=10
    def spawn(self,map):
        self.alive=True
        self.map=map
        self.coordonnates=(random.choice(range(self.map.size[0])),random.choice(range(self.map.size[1])))
        self.cursor=(random.choice(range(self.map.size[0])),random.choice(range(self.map.size[1])))
        self.speed=self.speed_constant
        self.mass=100
        self.grow()
        self.latest_move_time=time.time()
    def grow(self):
        self.size=sqrt(self.mass/math.pi) #A=pi*r^2
        self.hitbox=self.size/2
        f=self.view_factor=self.size*10
        self.view_field=(-f,-f,2*f,2*f)
    def draw(self,window,coordonnates):
        if self.skin is not None:
            self.skin.draw(window,coordonnates)
        (_x,_y)=self.coordonnates
        (x,y)=(int(_x),int(_y))
        pygame.draw.circle(window.screen, self.color, (x,y), int(self.size))
    def closest(self,entities):
        entities.remove(self)
        r=9999
        for _entity in entities:
            (x,y)=_entity.coordonnates
            _r=sqrt(x**2+y**2)
            if _r<r:
                entity=_entity
                r=min(r,_r)
        return entity
    def getPolar(self,cartesian):
        (x,y)=cartesian
        p=sqrt(x**2+y**2)
        o=math.atan(y/x)
        polar=(p,o)
        return polar
    def getCartesian(self,polar):
        (p,o)=polar
        (x,y)=(p*math.cos(o),p*math.sin(o))
        cartesian=(x,y)
        return cartesian
    def move(self):
        (cx,cy)=self.coordonnates
        (dx,dy)=self.cursor
        self.direction=(dx-cx,dy-cy)
        (p,o)=self.getPolar(self.direction)
        new_move_time=time.time()
        delta_time=new_move_time-self.latest_move_time
        self.latest_move_time=new_move_time
        self.speed=(self.speed_constant*delta_time)/self.mass
        p*=self.speed
        (px,py)=self.getCartesian((p,o))
        (cx,cy)=(px+cx,py+cy)
        self.coordonnates=(cx,cy)
    def spectate():
        pass
