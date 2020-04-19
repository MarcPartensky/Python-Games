from mygameengine import Game,Level
from mycontext import Context
from mycase import Case
import noise
import numpy as np
import mycolors
import random

class Expanse(Game):
    """Create an expanse game."""
    def __init__(self,context):
        """Create the game."""
        self.context=context
        #self.player=Case(0,0)
        self.levels=[ExpanseLevel()]
        self.stage=0

    def main(self):
        """Main loop of the game."""
        for level in self.levels:
            level.setContext(self.context)
            #level.setPlayer(self.player)
            level.main()

    def addLevel(self,level):
        """Add a level."""
        self.levels.append(level)


class ExpanseCase(Case):
    """Case of the game expanse."""
    def __init__(self,x,y,n):
        """Create an expanse case using the perlin noise number n."""
        super().__init__(x,y)
        self.createFromN(n)

    def createFromN(self,n):
        """Create an expanse case from n."""
        n+=0.5 #N is between 0 and 1
        if n<0.5:
            b=mycolors.bijection(n,[0,0.5],[0,255])
            self.color=(0,0,b)
        elif n<0.55:
            b=int(mycolors.bijection(n,[0.5,0.55],[150,50]))
            self.color=(255,255,b)
        elif n<0.8:
            if n%0.01>0.002:
                g=int(mycolors.bijection(n,[0.55,0.8],[255,100]))
                self.color=(10,g,10)
            else:
                self.color=(0,150,0)
        elif n<0.92:
            if n%0.01>0.001:
                g=int(mycolors.bijection(n,[0.8,0.92],[100,255]))
                self.color=(g,g,g)
            else:
                self.color=(0,50,0)
        else:
            self.color=mycolors.WHITE

    def show(self,context):
        x,y=self.position
        context.draw.rect(context.screen,self.color,(x,y,1,1),1)

class Player(Case):
    """Player of the game expanse. The class player inherits from case because
    it allow the players to be of the right size."""
    def __init__(self,*args,**kwargs):
        """Create a player."""
        super().__init__(*args,**kwargs)

    def update(self,events):
        """Update the player be giving him a copy of the map."""



class Map:
    """Create a map."""
    def __init__(self,size):
        """Create a map."""
        self.createGrid(size)

    def createGrid(self,size):
        """Convert the 2d perlin grid into a grid of cases."""
        sx,sy=size
        self.grid=[[None for y in range(sy)] for x in range(sx)]
        shape = (1024,1024)
        scale = 100.0
        octaves = 6
        persistence = 0.5
        lacunarity = 2.0
        for x in range(sx):
            for y in range(sy):
                n=noise.pnoise2(x/scale,
                                y/scale,
                                octaves=octaves,
                                persistence=persistence,
                                lacunarity=lacunarity,
                                repeatx=1024,
                                repeaty=1024,
                                base=0)
                self.grid[x][y] = ExpanseCase(x,y,n)

    def show(self,context):
        """Show the map within the given corners."""
        sx,sy=self.size
        xmin,ymin,xmax,ymax=context.corners
        xmin=int(xmin)
        ymin=int(ymin)
        xmax=int(xmax)+1
        ymax=int(ymax)+1
        for y in range(ymin,ymax+1):
            for x in range(xmin,xmax+1):
                if 0<=x<sx and 0<=y<sy:
                    self.grid[x][y].show(context)

    def getSize(self):
        """Return the size of the map using its grid."""
        sx=len(self.grid)
        sy=len(self.grid[0])
        return (sx,sy)

    size=property(getSize)

class ExpanseLevel:
    """Create a level."""
    def __init__(self,size=[200,200]):
        """Create a level."""
        self.map=Map(size)

    def setContext(self,context):
        """Set the context of the expanse level."""
        self.context=context

    def setPlayer(self,player):
        """Set the player of the expanse level."""
        self.player=player

    def main(self):
        """Main loop of the level."""
        while self.context.open:
            self.context.check()
            self.show()
            self.update()


    def update(self):
        """Update the level."""
        pass

    def show(self):
        """Show the level."""
        self.context.control()
        self.context.clear()
        self.context.show()
        self.map.show(self.context)
        self.context.flip()

if __name__=="__main__":
    context=Context(fullscreen=True,size=[1440,900])
    expanse=Expanse(context)
    expanse.main()
