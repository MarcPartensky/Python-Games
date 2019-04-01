from myplane import Plane
from mywindow import Window
from mycolors import WHITE

class Zone(Plane):
    def __init__(self,size=[20,20],theme={},view=None):
        Plane.__init__(self,theme,view)
        self.size=size
        if not "borders_color" in theme: self.theme["borders_color"]=(255,255,255)

    def show(self,window):
        """Show the zone on the screen's window."""
        self.showGrid(window)
        self.showBorders(window)

    def showBorders(self,window):
        """Show the borders with a different color."""
        px,py=self.position
        wsx,wsy=window.size
        ux,uy=self.units
        sx,sy=self.size
        nx=int(wsx/ux)
        ny=int(wsy/uy)
        #Get the edge of the plane's view in its coordonnates
        zx=-sx//2
        Zx= sx//2
        zy=-sy//2
        Zy= sy//2
        mx=max(int(-nx+px),zx)
        Mx=min(int( nx+px),Zx)
        my=max(int(-ny+py),zy)
        My=min(int( ny+py),Zy)
        #Show the lines only if they can be seen.
        lines=[]
        if -nx+px<=zx: lines.append([[zx,my],[zx,My]])
        if  nx+px>=Zx: lines.append([[Zx,my],[Zx,My]])
        if -ny+py<=zy: lines.append([[mx,zy],[Mx,zy]])
        if  ny+px>=Zy: lines.append([[mx,Zy],[Mx,Zy]])
        for line in lines:
            start,end=line
            start=self.getToScreen(start,window)
            end=  self.getToScreen(end,window)
            window.draw.line(window.screen,self.theme["borders_color"],start,end,1)

    def showGrid(self,window):
        """Show the grid using the window."""
        px,py=self.position
        wsx,wsy=window.size
        ux,uy=self.units
        sx,sy=self.size
        nx=int(wsx/ux)
        ny=int(wsy/uy)
        #Get the edge of the plane's view in its coordonnates
        mx=max(int(-nx+px),-sx//2)
        Mx=min(int(nx+px),sx//2)
        my=max(int(-ny+py),-sy//2)
        My=min(int(ny+py),sy//2)
        #For each line find the begining and the end in the plane's coordonnates then convert it into screen's coordonnates.
        for x in range(mx,Mx+1):
            color=self.getUnitsColor(x)
            start=[x,my]
            end=  [x,My]
            start=self.getToScreen(start,window)
            end=  self.getToScreen(end,window)
            window.draw.line(window.screen,color,start,end,1)
        #Repeat the process for the y component
        for y in range(my,My+1):
            color=self.getUnitsColor(y)
            start=[mx,y]
            end=  [Mx,y]
            start=self.getToScreen(start,window)
            end=  self.getToScreen(end,window)
            window.draw.line(window.screen,color,start,end,1)


if __name__=="__main__":
    window=Window(fullscreen=True)
    zone=Zone([10,10])
    zone(window)
