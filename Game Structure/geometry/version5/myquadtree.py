from collections import namedtuple
from myabstract import Point

import random
import mycolors

#Point = namedtuple('Point', ['x', 'y'])


def randomPoint():
    return Point(random.uniform(-1, 1), random.uniform(-1, 1))

def randintPoint():
    return Point(random.randint(-10, 10), random.randint(-10, 10))

n = 10
points = [randomPoint() for i in range(n)]


class QuadTree:
    @classmethod
    def random(cls,n,**kwargs):
        """Create a quadtree of 'n' points."""
        points = [Point.random() for i in range(n)]
        return cls(points,**kwargs)


    def __init__(self, points,
                 neighbors=1,
                 color=mycolors.WHITE,
                 depth=float('inf')):
        """Create a quadtree using its positions."""
        self.check(points)
        self.points = dict(zip(range(len(points)), points))
        self.neighbors = neighbors
        self.color = color
        self.depth = depth

    def check(self, points):
        """Determine the points are one upon another."""
        pts=[tuple(p) for p in points]
        if sorted(list(set(pts))) != sorted(pts):
            raise Exception("No point must be upon another.")

    def compute(self):
        """Compute all objects."""
        self.position = self.computePosition()
        self.length = self.computeLength()
        self.paths = {}
        self.tree = self.computeTree(self.points, self.position, self.length)

    def computePosition(self):
        """Compute the position of the quadtree."""
        xmin = min([p.x for p in self.points.values()])
        xmax = max([p.x for p in self.points.values()])
        ymin = min([p.y for p in self.points.values()])
        ymax = max([p.y for p in self.points.values()])
        x = (xmax + xmin) / 2
        y = (ymax + ymin) / 2
        return [x, y]

    def computeLength(self):
        """Compute the length of the quadtree."""
        xmin = min([p.x for p in self.points.values()])
        xmax = max([p.x for p in self.points.values()])
        ymin = min([p.y for p in self.points.values()])
        ymax = max([p.y for p in self.points.values()])
        return max(xmax - xmin, ymax - ymin)

    def __str__(self):
        return "QuadTree("+str(self.getDictionary(self.tree))+")"


    def getDictionary(self,tree):
        """Return the tree under the dictionary syntax using the tree in
        the None syntax."""
        cdb=True
        for e in tree:
            if isinstance(e,list):
                cdb=False
        if cdb:
            return tree
        else:
            d={}
            for i,e in enumerate(tree):
                if e is not None:
                    d[i]=self.getDictionary(e)
            return d

    def computeTree(self, points, position, length, n=0, path=[]):
        """Find the sub trees."""
        if len(points) == 0:
            return None
        elif len(points) <= self.neighbors or n > self.depth:
            for key in points:
                self.paths[key] = path
            return list(points.keys())
        else:
            x, y = position
            l = length
            pos1 = (x - l / 4, y + l / 4)
            pos2 = (x + l / 4, y + l / 4)
            pos3 = (x - l / 4, y - l / 4)
            pos4 = (x + l / 4, y - l / 4)
            pts1, pts2, pts3, pts4 = [], [], [], []

            for key, pt in points.items():
                if pt.x > x:
                    if pt.y > y:
                        pts2.append((key, pt))
                    else:
                        pts4.append((key, pt))
                else:
                    if pt.y > y:
                        pts1.append((key, pt))
                    else:
                        pts3.append((key, pt))

            pts1 = dict(pts1)
            pts2 = dict(pts2)
            pts3 = dict(pts3)
            pts4 = dict(pts4)

            return [self.computeTree(pts1, pos1, l/2, n+1, path+[0]),
                    self.computeTree(pts2, pos2, l/2, n+1, path+[1]),
                    self.computeTree(pts3, pos3, l/2, n+1, path+[2]),
                    self.computeTree(pts4, pos4, l/2, n+1, path+[3])]

    def getPoints(self, index, radius):
        """Return the list of points that are in the circle of center the point
        of index 'index' and radius 'radius'."""


        return pts

    def getSquare(self):
        """Return all the squares of the paths."""
        squares=[]
        for path in self.paths:
            length=self.length/2**len(path)
            l=self.length
            x,y=self.position
            for level in path:
                if level==0:
                    x-=l/level
                    y+=l/level
                elif level==1:
                    x+=l/level
                    y+=l/level
                elif level==2:
                    x-=l/level
                    y-=l/level
                else:
                    x+=l/level
                    y-=l/level
            squares.append(((x,y),length))
        return squares


    def show(self,context):
        """Show the quadtree."""
        self.showTree(context,self.tree,self.position,self.length/2)
        self.showPoints(context)

    def showPoints(self,context):
        """Show each point."""
        for point in self.points.values():
            point.show(context)

    def showTree(self,context,tree,position,length):
        """Show the given trees recusively."""
        if isinstance(tree,list):
            #Unpack the values
            x,y=position
            l=length
            #Show a square
            points=[(x-l,y+l),(x+l,y+l),(x+l,y-l),(x-l,y-l)]
            context.draw.lines(context.screen,self.color,points)
            #Show the trees
            if len(tree)>=1:
                self.showTree(context,tree[0],(x-l/2,y+l/2),l/2)
            if len(tree)>=2:
                self.showTree(context,tree[1],(x+l/2,y+l/2),l/2)
            if len(tree)>=3:
                self.showTree(context,tree[2],(x-l/2,y-l/2),l/2)
            if len(tree)>=4:
                self.showTree(context,tree[3],(x+l/2,y-l/2),l/2)


if __name__ == "__main__":
    from mymanager import Manager
    from mymotion import Motion

    class QuadtreeManager(Manager):
        @classmethod
        def random(cls,n=50):
            """Create a quadtree of 'n' points."""
            return cls(QuadTree.random(n=n))

        def __init__(self,quadtree,name="Quadtree Manager"):
            """Create a quadtree manager using the quadtree."""
            super().__init__(name=name)
            self.quadtree=quadtree
            self.quadtree.compute()

        def show(self):
            """Show the quadtree."""
            self.quadtree.show(self.context)

    class QuadtreeTester(Manager):
        @classmethod
        def random(cls,n=50,**kwargs):
            """Create a quadtree of 'n' points."""
            motions=[Motion.random(n=2) for i in range(n)]
            return cls(motions,**kwargs)

        def __init__(self,motions,name="Quadtree Manager",**kwargs):
            """Create a quadtree manager using the quadtree."""
            super().__init__(name=name,**kwargs)
            self.motions=motions

        def update(self):
            """Update the motions and in consequence the quadtree."""
            self.updateMotions()
            self.quadtree=QuadTree(self.points)
            self.quadtree.compute()

        def updateMotions(self):
            """Update the motions."""
            for motion in self.motions:
                motion.update(self.dt)

        def show(self):
            """Show the quadtree."""
            self.quadtree.show(self.context)

        @property
        def points(self):
            """Return the points at the positions of the motions."""
            return [Point(*m.position) for m in self.motions]

    qm=QuadtreeTester.random(n=200,fullscreen=True)
    qm()
