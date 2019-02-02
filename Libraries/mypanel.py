from mycolors import *
from mywindow import Window

class Panel:
    def __init__(self,name="Unnamed Pannel",window=None,position=None,size=None,background=BLACK,border=WHITE):
        """Create panel object."""
        self.window=window
        self.position=position
        self.size=size
        self.load()
        #if window is not None:
        #    self.loadFromWindow(window)

    def load(self):
        """Load panel object."""
        self.background=BLUE
        self.border=WHITE
        self.default_size=[100,100]

    def loadFromWindow(self,window):
        """Load windows attributs."""
        x,y,sx,sy=self.center(window,self.default_size)
        self.position=(x,y)
        self.size=(sx,sy)

    def center(self,window):
        """Center object by default."""
        wsx,wsy=window.size
        wcx,wcy,wcsx,wcsy=window.coordonnates
        hx,hy=(wcsx-wcx,wcsy-wcy)
        return (hx,hy,wsx,wsy)

    def show(self,window,coordonnates,background_color,border_color):
        """Show pannel on screen."""
        #if coordonnates is None:
        #coordonnates=self.position+self.size
        #background=self.background
        #border=self.border
        #print(background,coordonnates)
        x,y,sx,sy=coordonnates
        pygame.draw.rect(window.screen,background_color,(x,y,sx,sy),0)
        pygame.draw.line(window.screen,border_color,(x,y),(x,y+sy),1)
        pygame.draw.line(window.screen,border_color,(x,y+sy),(x+sx,y+sy),1)
        pygame.draw.line(window.screen,border_color,(x+sx,y+sy),(x+sx,y),1)
        pygame.draw.line(window.screen,border_color,(x+sx,y),(x,y),1)

    def createButtons(self,names):
        """Create button entities for pannel."""
        for i in range(len(names)):
            self.buttons.append(Button(names[i]))

    def checkButtons(self):
        """Return buttons states."""
        states=[]
        for button in self.buttons:
            states.append(button())
        return states




if __name__=="__main__":
    w=Window("Testing pannel")
    p=Panel(w)
    p.show(w,[100,100,400,400],BLUE,GREEN)
    w.flip()
    w.pause()
