class Plan:
    def __init__(self,size=[10,10],zoom=[1,1],position=[0,0],color_background=(0,0,0),color_line=(255,255,255),graduate=False):
        self.size=size
        self.zoom=zoom
        self.color_background=color_background
        self.color_line=line
        self.graduate=graduate
    def draw(self,window):
        window.clear(color_background)
        wsx,wsy=window.size
