from mylab import Lab
from rectangle import Rectangle
from random import randint as rdt

class Room(Lab):
    def __init__(self):
        self.name="Camera tests"
        Lab.__init__(self,self.name)
        wsx,wsy=self.window.size
        self.window.text_size=30
        self.window.build()
        size=[wsx//2,wsy//2]
        position=[rdt(0,wsx//2),rdt(0,wsy//2)]
        borders=[0,0]+self.window.size
        friction=0.1
        entity=Rectangle(position=position,size=size,borders=borders,friction=friction,controllable=True)
        entity.duplicate(5)
        self.entities=[entity]



if __name__=="__main__":
    print(1)
    r=Room()
    print(2)
    r()
    r.window.pause()
