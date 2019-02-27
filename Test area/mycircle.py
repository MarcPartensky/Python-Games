import myentity

class Circle(Entity):
    def __init__(self,radius=50):
        Entity.__init__(self,dimensions=2)
        self.radius=radius
        
