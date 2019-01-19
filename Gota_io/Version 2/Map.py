BLUE    = (  0,  0,255)
RED     = (255,  0,  0)
YELLOW  = (255,255,  0)
BLACK   = (  0,  0,  0)
GREY    = (127,127,127)
WHITE   = (255,255,255)
COLORS=[BLACK,WHITE,RED,YELLOW,BLUE]

class Map:
    def __init__(self,size=(100,100),colors=(BLACK,GREY,WHITE)):
        self.colors=(self.background_color,self.axes_color,self.borders_color)=colors
        self.size=size
        self.map=np.zeros(self.size)
