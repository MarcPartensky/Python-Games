from mydraw import Draw
from mywindow import Window

class Surface:
    def __init__(self,draw=None,**kwargs):
        """Create a surface."""
        if not draw: self.draw=Draw(**kwargs)
        else: self.draw=draw
        self.screen=self.draw.window.screen
        self.open=self.draw.window.open
        self.clear=self.draw.clear
        self.flip=self.draw.window.flip
        self.press=self.draw.window.press
        self.build=self.draw.window.build
        self.click=self.draw.window.click
        self.__call__=self.draw.window.__call__
        self.wait=self.draw.window.wait
        #self.show=self.draw.show
        self.control=self.draw.control

    def point(self):
        """Adapt the position of the cursor in plane's coordonnates."""
        x,y=self.draw.window.point()
        x,y=self.draw.plane.getFromScreen([x,y],self.draw.window)
        return (x,y)

    def check(self):
        """Check if the surface is open."""
        self.draw.window.check()
        self.open=self.draw.window.open

    def __call__(self):
        """Calling the surface allow the user to move on screen."""
        while self.open:
            self.check()
            self.draw.plane.control(self.draw.window)
            self.draw.window.clear()
            self.draw.plane.show(self.draw.window)
            self.flip()

    def show(self):
        """Show the plane on screen."""
        self.draw.plane.show(self.draw.window)

    def print(self,text,position,**kwargs):
        """Print a text the window's screen using text and position and optional arguments."""
        position=self.draw.plane.getToScreen(position,self.draw.window)
        self.draw.window.print(text,position,**kwargs)

    def getCorners(self):
        """Return the corners of the plane."""
        corners=self.draw.plane.getPlaneCorners(self.draw.window)
        return corners

    def controlZoom(self):
        """Control the zoom of the surface's plane."""
        self.draw.plane.controlZoom(self.draw.window)

    def controlPosition(self):
        """Control the position of the surface's plane."""
        self.draw.plane.controlPosition(self.draw.window)

    def getFromScreen(self,position):
        """Behave like the get from screen of the plan without having to put the window in parameter."""
        return self.draw.plane.getFromScreen(position,self.draw.window)



class Surface2(Window):
    def __init__(self,*args,**kwargs):
        Window.__init__(self,*args,**kwargs)
        self.draw=Draw()



if __name__=="__main__":
    surface=Surface()
    #surface()
    #pass
