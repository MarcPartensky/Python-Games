from mywindow import Window
from pygame.locals import *

class Plane:
    def __init__(self,theme={},view=None):
        """Create a plane using optionals theme and view."""
        self.createTheme(theme)
        self.createView(view)

    def createTheme(self,theme={}):
        """Initializes the position and the colors for the view of the plane using optional theme."""
        if not "background" in theme: theme["background"]= (0,0,0)
        if not "grid"       in theme: theme["grid"]=       [(100,100,100),(50,50,50),(10,10,10)]
        self.theme=theme

    def createView(self,view=None):
        """Initializes the position and the units for the view of the plane using optional view."""
        """View must be a list of length 2."""
        if view:
            self.position= view[0]
            self.units=    view[1]
            self.default_position= view[0][:]
            self.default_units=    view[1][:]
        else:
            self.default_position= [ 0, 0]   #position of the center of the view in the plane's coordonnates
            self.default_units=    [40,40]   #units of the conversion from window/plane
            self.position=         [ 0, 0]
            self.units=            [40,40]

    def __call__(self,window): #The main loop must be redefined by the client and not the functions called within it.
        """Main loop of the plane."""
        window.rename("Plane")
        while window.open:
            window.check()
            self.control(window)
            self.clear(window)
            self.show(window)
            self.flip(window)

    def flip(self,window):
        """Flip the plane's window."""
        window.flip()

    def clear(self,window):
        """Clear the plane."""
        window.clear(self.theme["background"])

    def control(self,window):
        """Control the view of the plane."""
        ux,uy=self.units
        keys=window.press()
        if keys[K_RSHIFT]:
            self.zoom([1.1,1.1])
        if keys[K_LSHIFT] and (ux>2 and uy>2):
            self.zoom([0.9,0.9])
        if keys[K_RETURN]:
            self.units=    self.default_units[:]
            self.position= self.default_position[:]
        k=50 #Allow the user to move in the grid a reasonable velocity.
        if keys[K_LEFT]:
            self.position[0]-=window.size[0]/self.units[0]/k
        if keys[K_RIGHT]:
            self.position[0]+=window.size[0]/self.units[0]/k
        if keys[K_DOWN]:
            self.position[1]-=window.size[1]/self.units[1]/k
        if keys[K_UP]:
            self.position[1]+=window.size[1]/self.units[1]/k

    def getUnitsColor(self,x):
        """Get the color given a x position."""
        if x%100==0:
            return self.theme["grid"][0]
        elif x%10==0:
            return self.theme["grid"][1]
        else:
            return self.theme["grid"][2]

    def show(self,window):
        """Show the elements on screen using the window."""
        self.showGrid(window)
        #self.showUnits(window) #Does not work for now


    def showUnits(self,window): #Not working because of error of synchronisation between text base system and normal window base.
        """Show the unit of the grid using the window."""
        px,py=self.position
        wsx,wsy=window.size
        ux,uy=self.units
        nx=int(wsx/ux)
        ny=int(wsy/uy)
        for y in range(int(-ny+py),int(ny+py)+1,10):
            for x in range(int(-nx+px),int(nx+px)+1,10):
                X,Y=self.getToScreen([x,y],window)
                window.print(str([x,y]),[X,Y],size=20)

    def showGrid(self,window):
        """Show the grid using the window."""
        px,py=self.position
        wsx,wsy=window.size
        ux,uy=self.units
        nx=int(wsx/ux)
        ny=int(wsy/uy)
        #Get the edge of the plane's view in its coordonnates
        mx=int(-nx+px)
        Mx=int(nx+px)
        my=int(-ny+py)
        My=int(ny+py)
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

    def zoom(self,zoom):
        """Allow the user to zoom into the plane."""
        for i in range(2):
            self.units[i]*=zoom[i]

    def getToScreen(self,position,window):
        """Return a screen position using a position in the plane."""
        x,y=position[0],position[1]
        px,py=self.position
        ux,uy=self.units
        wsx,wsy=window.size
        x=int((x-px)*ux+wsx/2)
        y=int(wsy/2-(y-py)*uy)
        return [x,y]

    def getAllToScreen(self,positions,window):
        """Return the list of screen positions using the list of plane positions."""
        screen_positions=[]
        for position in positions:
            screen_positions.append(self.getToScreen(position,window))
        return screen_positions

    def getFromScreen(self,position,window):
        """Return a plane position using a a position in the screen."""
        x,y=position[0],position[1]
        px,py=self.position
        ux,uy=self.units
        wsx,wsy=window.size
        x=(x-wsx/2)/ux+px
        y=(wsy/2-y)/uy+py
        return [x,y]

    def getAllFromScreen(self,position,window):
        """Return the list of plane positions using the list of screen positions."""
        plane_positions=[]
        for position in positions:
            planes_positions.append(self.getFromScreen(position,window))
        return plane_positions

if __name__=="__main__":
    window=Window(fullscreen=True)
    theme={"background":(0,0,0)}
    plane=Plane(theme)
    plane(window)
