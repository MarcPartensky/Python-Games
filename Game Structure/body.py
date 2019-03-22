class Body(Form)
    def __init__(self,physics,points):
        Form.__init__(self,points)
        position,velocity,acceleration=physics
        self.position=position
        self.velocity=velocity
        self.acceleration=acceleration
    def move(self,time=1):
        for i in range(len(self.position)):
            self.velocity[i]+=self.acceleration[i]*time
            self.position[i]+=self.velocity[i]*time
