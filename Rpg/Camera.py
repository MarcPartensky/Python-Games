class Camera:
    def __init__(self,position=None,size=None,zoom=[1,1]):
        self.position=position
        self.velocity=velocity
        self.acceleration=acceleration
        self.size=size
        self.zoom=zoom
    def adjust(self,position):
        self.position=position
        return position

    def __call__(self):
        pass
