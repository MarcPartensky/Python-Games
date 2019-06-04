from mydraw import Draw
from mywindow import Window

import mycolors

class Surface:
    """Might inherit from Rect soon..."""
    
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
        self.control=self.draw.control

    def getKeys(self):
        """Return the keys of the window."""
        return self.press()

    def getCorners(self):
        """Return the corners of the surface shown."""
        return self.draw.plane.getCorners(self.draw.window)

    def setCorners(self,corners):
        """Set the corners of the plane using the new corners."""
        self.draw.plane.setCorners(corners,self.draw.window)

    def getRect(self):
        """Return the rect of the surface shown."""
        return Plane.getRectFromCorners(self.getCorners())

    def setRect(self,rect):
        """Set the rect of the surface shown."""
        self.draw.plane.setCorners(Plane.getCornersFromRect(rect))

    def getCoordonnates(self):
        """Return the coordonnates of the surface shown."""
        return Plane.getCoordonnatesFromCorners(self.getCorners())

    def setCoordonnates(self,coordonnates):
        """Set the coordonnates of the surface shown."""
        self.draw.plane.setCorners(Plane.getCornersFromCoordonnates(coordonnates))

    def getPosition(self):
        """Return the position of the surface shown."""
        return self.draw.plane.position

    def setPosition(self,position):
        """Set the position of the surface shown."""
        self.draw.plane.position=position

    def getSize(self):
        """Return the size of the surface shown."""
        return self.draw.plane.getSize()

    def setSize(self,size):
        """Set the size of the surface shown."""
        self.draw.plane.setSize(size)

    def getUnits(self):
        """Return the units of the surface shown."""
        return self.draw.plane.units

    def setUnits(self,units):
        """Set the units of the surface shown."""
        self.draw.plane.units=units

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

    def print(self,text,position,text_size=1,color=mycolors.WHITE,font=None,conversion=True):
        """Print a text the window's screen using text and position and optional
        color, pygame font and conversion."""
        position=self.draw.plane.getToScreen(position,self.draw.window)
        ux,uy=self.draw.plane.units
        if conversion: text_size=int(text_size*ux/50)
        self.draw.window.print(text,position,text_size,color,font)

    def controlZoom(self):
        """Control the zoom of the surface's plane."""
        self.draw.plane.controlZoom(self.draw.window)

    def controlPosition(self):
        """Control the position of the surface's plane."""
        self.draw.plane.controlPosition(self.draw.window)

    def getFromScreen(self,position):
        """Behave like the get from screen of the plan without having to put the window in parameter."""
        return self.draw.plane.getFromScreen(position,self.draw.window)

    def __enter__(self):
        """Opening the context."""
        self.check()
        self.control()
        self.clear()
        self.show()
        print("went in")
        return self

    def __exit__(self):
        """Ending the context."""
        print("going out")
        self.flip()
        if self.open:
            self.__enter__()

    corners=property(getCorners,setCorners,"Allow the user to manipulate the corners of the surface easily.")
    rect=property(getRect,setRect,"Allow the user to manipulate the rect of the surface easily.")
    coordonnates=property(getCoordonnates,setCoordonnates,"Allow the user to manipulate the coordonnates of the surface easily.")
    position=property(getPosition,setPosition,"Allow the user to manipulate the position of the surface easily.")
    size=property(getSize,setSize,"Allow the user to manipulate the size of the surface easily.")
    units=property(getUnits,setUnits,"Allow the user to manipulate the units of the surface easily.")
    keys=property(getKeys,"Allow the user to manipulate the keys of the surface easily.")


Context=Surface


if __name__=="__main__":
    context=Context()
    context()
