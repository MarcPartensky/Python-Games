from mylab import Lab
from mycamera import Camera

class Room(Lab):
    def __init__(self):
        Lab.__init__(self)
        self.camera=Camera(position=[0,0],size=[10,10],borders=[0,0,10,10])
        self.entities.append(self.camera)






if __name__=="__main__":
    r=Room()
    r()
