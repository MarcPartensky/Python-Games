class Connector: #supposed to be the mother class of all objects needing 2 points to be defined as lines and segments.
    def __init__(self,point,vector):
        self.point=point
        self.vector=vector
    def angle(self):
        return vector.angle()
