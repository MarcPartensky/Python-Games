from mywindow import Window
from pygame.locals import *

class Plane:
    def __init__(self,theme=None,view=None):
        """Create a plane using te"""
        self.createTheme(theme)
        self.createView(view)
        self.warnings=[0,0,0]

    def createTheme(self,theme=None):
        """Initializes the position and the colors for the view of the plane using optional theme."""
        if theme:
            self.background_color= theme[0]
            self.grid_colors=      theme[1]
        else:
            self.background_color= (  0,  0,  0)
            self.grid_colors=      (255,255,255) #Still not applied because of the cool effect of different colors for different units scales

    def createView(self,view=None):
        """Initializes the position and the units for the view of the plane using optional view."""
        if view:
            self.position= view[0]
            self.units=    view[1]
        else:
            self.default_position= [ 0, 0]   #position of the center of the view in the plane's coordonnates
            self.default_units=    [40,40]   #units of the conversion from window/plane
            self.position=         [ 0, 0]
            self.units=            [40,40]

    def __call__(self,window):
        """Main loop of the plane."""
        window.rename("Plane")
        while window.open:
            window.check()
            self.eventsPlane(window)
            self.event(window)  #To overload by the client
            self.update(window) #To overload by the client
            self.showPlane(window)
            self.show(window)   #To overload by the client
            window.flip()

    def update(self,window):
        """Method to be overloaded in other programs."""
        if not self.warnings[0]:
            self.warnings[0]=1
            print("The update method needs to be overloaded.")

    def event(self,window):
        """Method to be overloaded in other programs."""
        if not self.warnings[1]:
            self.warnings[1]=1
            print("The event method needs to be overloaded.")

    def show(self,window):
        """Method to be overloaded in other programs."""
        if not self.warnings[2]:
            self.warnings[2]=1
            print("The show method needs to be overloaded.")

    def eventsPlane(self,window):
        """Deal with the plane events."""
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

    def showPlane(self,window):
        """Show the elements on screen using the window."""
        window.clear(self.background_color)
        self.showGrid(window)
        #self.showUnits(window) #Does not work


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
        ofx,ofy=2,2 #x and y offset
        #Find the lines in plane's base to draw using position, units and window size and then convert them
        for x in range(int(-nx+px)-ofx,int(nx+px)+ofx):
            if x%100==0: color=(100,100,100)
            elif x%10==0: color=(50,50,50)
            else: color=(20,20,20)
            start=[x,int(-ny/2+py)-ofy]
            end=  [x,int( ny/2+py)+ofy]
            start=self.getToScreen(start,window)
            end=  self.getToScreen(end,window)
            window.draw.line(window.screen,color,start,end,1)
        #Repeat the process for the y component
        for y in range(int(-ny+py)-ofy,int(ny+py)+ofy):
            if y%100==0: color=(100,100,100)
            elif y%10==0: color=(50,50,50)
            else: color=(20,20,20)
            start=[int(-nx/2+px)-ofx,y]
            end=  [int( nx/2+px)+ofx,y]
            start=self.getToScreen(start,window)
            end=  self.getToScreen(end,window)
            window.draw.line(window.screen,color,start,end,1)

    def zoom(self,zoom):
        """Allow the user to zoom into the plane."""
        for i in range(2):
            self.units[i]*=zoom[i]

    def getToScreen(self,position,window):
        """Return a position in the screen using a position in the plane."""
        x,y=position[0],position[1]
        px,py=self.position
        ux,uy=self.units
        wsx,wsy=window.size
        x=int((x-px)*ux+wsx/2)
        y=int(wsy/2-(y-py)*uy)
        return [x,y]

    def getFromScreen(self,position,window):
        """Return a position in the plane using a a position in the window."""
        x,y=position[0],position[1]
        px,py=self.position
        ux,uy=self.units
        wsx,wsy=window.size
        x=(x-wsx/2)/ux+px
        y=(wsy/2-y)/uy+py
        return [x,y]

if __name__=="__main__":
    window=Window(fullscreen=True)
    plane=Plane()
    plane(window)
