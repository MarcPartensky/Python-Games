from mywindow import Window
from pygame.locals import *

class Plan:
    def __init__(self,theme=None,view=None):
        if not theme:
            self.createTheme()
        if not view:
            self.createView()
    def createTheme(self):
        self.theme={"background color": (0,0,0),
                    "grid color":       (255,255,255)}
    def createView(self):
        self.position=[0,0]     #position of the center of the view in the plan's coordonnates
        self.size=[10,10]       #size of the view in the plan's coordonnates
        self.units=[50,50]      #units of the conversion from window/plan
    def __call__(self,window):
        while window.open:
            window.check()
            self.event(window)
            #self.update(window)
            self.show(window)
    def event(self,window):
        keys=window.press()
        if keys[K_q]:
            zoom=[1.01,1.01]
            self.zoom(zoom)
        if keys[K_a]:
            zoom=[0.99,0.99]
            self.zoom(zoom)
        if keys[K_LEFT]:
            self.position[0]-=1
        if keys[K_RIGHT]:
            self.position[0]+=1
        if keys[K_DOWN]:
            self.position[1]+=1
        if keys[K_UP]:
            self.position[1]-=1

    def show(self,window):
        window.clear(self.theme["background color"])
        self.showGrid(window)
        window.flip()
    def showGrid(self,window,color=None):
        if not color:
            color=self.theme["grid color"]
        wsx,wsy=window.size
        sx,sy=self.size
        ux,uy=self.units
        zx=ux/sx
        zy=uy/sy
        [mx,my],[Mx,My]=Plan.positionToCorners(self.position,self.size)
        #dx=mx-int(mx)
        #lx=[ix+dx for ix in range(int(mx),int(Mx)+1)]
        pwmx,pwmy=self.getFromScreen([0,0])
        pwMx,pwMy=self.getFromScreen([wsx,wsy])
        nx=(pwMx-pwmx)/zx
        ny=(pwMy-pwmy)/zy
        for i in range(int(nx)+1):
            x=pwmx+i*zx
            start=[x,pwmy]
            end=  [x,pwMy]
            print(start,end)
            start=self.getToScreen(start)
            end=  self.getToScreen(end)
            window.draw.line(window.screen,color,start,end,1)
        #dy=my-int(my)
        #ly=[iy+dy for iy in range(int(my),int(My)+1)]
        for i in range(int(ny)+1):
            y=pwmy+i*zy
            start=[pwmx,y]
            end=  [pwMx,y]
            start=self.getToScreen(start)
            end=  self.getToScreen(end)
            window.draw.line(window.screen,color,start,end,1)
    def zoom(self,zoom):
        for i in range(2):
            self.size[i]*=zoom[i]
    def positionToCorners(position,size):
        x,y=position
        sx,sy=size
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
    def getToScreen(self,position):
        """Return a position in the screen using a position in the plan."""
        px,py=position
        x,y=self.position
        sx,sy=self.size
        ux,uy=self.units
        zx,zy=ux/sx,uy/sy
        [mx,my],[Mx,My]=Plan.positionToCorners(self.position,self.size)
        px=int((px-mx)*zx)
        py=int((py-my)*zy)

        return [px,py]
    def getFromScreen(self,position):
        """Return a position in the plan using a a position in the window."""
        px,py=position
        x,y=self.position
        sx,sy=self.size
        ux,uy=self.units
        zx,zy=ux/sx,uy/sy
        [mx,my],[Mx,My]=Plan.positionToCorners(self.position,self.size)
        px=int(px/zx-mx)
        py=int(py/zy-my)
        return [px,py]

if __name__=="__main__":
    window=Window()
    plan=Plan()
    print(Plan.positionToCorners(plan.position,plan.size))
    print(plan.getToScreen([5,2]))
    plan(window)
