from mywindow import Window

class Plan:
    def __init__(self,theme=None,view=None):
        if not theme:
            self.createTheme()
        if not view:
            self.createView()
    def createTheme(self):
        self.theme={"background color": (0,0,0),
                    "line color":       (255,255,255)}
    def createView(self):
        self.position=[0,0]     #position of the center of the view in the plan's coordonnates
        self.size=[10,15]       #size of the view in the plan's coordonnates
        self.scale=50           #scale of the view from the plan's coordonnates to the window size in pixels
        self.velocity=[0,0]     #velocity of the center of the view in the plan's coordonnates
        self.friction=[0.1,0.1] #friction applied to the velocity
    def __call__(self,window):
        while window.open:
            window.check()
            self.update(window)
            self.show(window)
    def show(self,window):
        window.clear(self.theme["background_color"])
        self.drawLines()
        window.flip()
    def zoom(self,zoom):
        for i in range(2):
            self.size[i]*=zoom[i]
    def positionToCorners(position,size):
        x,y=*position
        sx,sy=*size
        mx=x-sx/2
        my=y-sy/2
        Mx=sx+mx
        My=sy+my
        return [[mx,my],[Mx,My]]
    def cornersToPosition(minimum,maximum):
        mx,my=minimum
        Mx,My=maximum
        sx=Mx-mx
        sy=My-my
        x=mx+sx/2
        y=my+sy/2
        return [[x,y],[sx,sy]]
    def screenToPlan(self,position,size):
        mx,my,Mx,My=Plan.getCorners(position,size)
        x,y=position
        return [x,y]
    def planToScreen(position):
        mx,my,Mx,My=Plan.getCorners(position,size)
        x,y=self.position
        return



    def move(self,t=0.01):
        vx,vy=self.velocity
        fx,fy=self.friction
        x,y=self.position
        vx*=(1-fx)
        vy*=(1-fy)
        x+=vx*t
        y+=vy*t
        self.velocity=[vx,vy]
        self.position=[x,y]

    def update(self,window):
        pass

if __name__=="__main__":
    window=Window()
    plan=Plan()
    plan(window)
