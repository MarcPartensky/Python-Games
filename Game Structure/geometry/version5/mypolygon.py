class Polygon:
    def __init__(self,points,fill=False,width=1,color=WHITE,showpoints=True):
        """Create the polygon using points, fill, width, color and showpoints."""
        self.points=points
        self.fill=fill
        self.width=1
        self.color=color
        self.showpoints=showpoints
    def show(self,context):
        """Show the polygon using the context."""
        positions=[[p.x,p.y] for p in self.points]
        window.draw.polygon(context.screen,self.color,positions,self.width)
        if self.showpoints:
            for point in self.points:
                point.show(window)
