class Line:
    def __init__(self,point,vector,width=1,color=(255,255,255)):
        """Create the line using a point and a vector with optional width and color."""
        self.p=point
        vector.normalize()
        self.v=
