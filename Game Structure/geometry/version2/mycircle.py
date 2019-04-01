from mywindow import Window

class Circle:
    def __init__(self,x,y,radius,color=(255,255,255),width=1):
        """Create a circle object using x, y and radius and optional color and width."""
        self.x=x
        self.y=y
        self.radius=radius
        self.color=color
        self.width=width
    def show(self,window,color=None,width=None):
        """Show the circle on screen using the window."""
        if not color: color=self.color
        if not width: width=self.width
        window.draw.circle(window.screen,color,[self.x,self.y],self.radius,width)
    def __call__(self):
        """Return all coordonnates of the circle."""
        return [self.x,self.y,self.radius]

if __name__=="__main__":
    window=Window("Circles")
    c=Circle(400,200,20,(255,0,0))
    c.show(window)
    window()
