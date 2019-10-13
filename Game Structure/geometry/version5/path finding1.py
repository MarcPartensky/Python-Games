import cv2
import time
import random
import math

sj="saint jalm.jpg"
vl="valentin.png"
tm="tetedemarc.png"
pm="profiledemarc.jpg"

class Entity:
    def __init__(self,x,y,r,mr=8):
        self.x=x
        self.y=y
        self.r=r
        self.mr=mr
    def __str__(self):
        return "Entity("+",".join(map(str,[self.x,self.y,self.r]))+")"
    def turnRight(self,r=1):
        self.r=(self.r+r)%self.mr
    def turnLeft(self,r=1):
        self.r=(self.r+self.mr-r)%self.mr
    def turnBack(self):
        self.r=(self.r+self.mr//2)%self.mr
    def stepForward(self,p=1):
        if self.r==0:
            self.x+=p
        elif self.r==1:
            self.x+=p
            self.y+=p
        elif self.r==2:
            self.y+=p
        elif self.r==3:
            self.x-=p
            self.y+=p
        elif self.r==4:
            self.x-=p
        elif self.r==5:
            self.x-=p
            self.y-=p
        elif self.r==6:
            self.y-=p
        else: #self.r==7
            self.x+=p
            self.y-=p
    def stepBack(self,p=1):
        self.turnBack()
        self.stepForward(p)
        self.turnBack()
    def stepRight(self,p=1,r=1):
        self.turnRight(r)
        self.stepForward(p)
        self.turnLeft(r)
    def stepLeft(self,p=1,r=1):
        self.turnLeft(r)
        self.stepForward(p)
        self.turnRight(r)
    def stepRightReverse(self,p=1,r=1):
        self.turnRight(r)
        self.stepBack(p)
        self.turnLeft(r)
    def stepLeftReverse(self,p=1,r=1):
        self.turnLeft(r)
        self.stepBack(p)
        self.turnRight(r)
    def getPosition(self):
        return (self.x,self.y)
    def getComponents(self):
        return (self.x,self.y,self.r)

    position=property(getPosition)
    components=property(getComponents)


class Solver:
    """Solve a maze with an entity that can explore it."""
    def __init__(self,entity,maze):
        """Create a solver from an entity and a maze."""
        self.entity=entity
        self.maze=maze
        self.path=[]

    def solve(self):
        "Return the path made by the entity after exploring the maze."""
        self.explore(500)
        start=self.entity.components
        self.path=[self.entity.position]
        self.explore()
        while start!=self.entity.components:
            self.explore()

    def explore(self,n=1):
        """Explore the maze by taking 1 action and saving it."""
        for i in range(n):
            if self.lookRight():
                self.entity.turnRight()
            elif self.lookForward():
                self.entity.stepForward()
            else:
                self.entity.turnLeft()
            self.path.append(self.entity.position)

    def lookRight(self):
        """Determine if the case of the maze at the right of the entity is available."""
        self.entity.stepRight()
        x,y=self.entity.position
        available=self.isAvailable()
        self.entity.stepRightReverse()
        return available

    def lookLeft(self):
        """Determine if the case of the maze at the left of the entity is available."""
        self.entity.stepLeft()
        x,y=self.entity.position
        available=self.isAvailable()
        self.entity.stepLeftReverse()
        return available

    def lookForward(self):
        """Determine if the case of the maze at the front of the entity is available."""
        self.entity.stepForward()
        available=self.isAvailable()
        self.entity.stepBack()
        return available

    def isAvailable(self):
        """Determine if the entity is still within the maze."""
        try:
            x,y=self.entity.position
            return bool(self.maze[y][x])
        except:
            return False

    def getEntity(self):
        return self.entity
    def getMaze(self):
        return self.maze

    e=property(getEntity)
    m=property(getMaze)



image=cv2.imread(vl)
canny=cv2.Canny(image,50,150)

def searchPoints(canny_image):
    """Return the list of white points of a canny image."""
    l=[]
    height,width=image.shape[:2]
    for x in range(width):
        for y in range(height):
            if canny_image[y][x]:
                l.append((x,y))
    return l

def makeDictionary(pts):
    d={}
    for (x,y) in pts:
        d[y]={x:1}
    return d


points=searchPoints(canny)
print(len(points))

def solvePoints(pts,m=100):
    gs=[]
    while len(gs)<m and len(pts)>0:
        print(100*len(gs)/m,"%")
        x,y=pts[0]
        d=makeDictionary(pts)
        e=Entity(x,y,0)
        s=Solver(e,d)
        s.solve()
        a=set(s.path)
        p=set(pts)
        pts=list(p-a)
        gs.append(a)
    return (gs,pts)

def distance(p1,p2):
    """Return the distance of the points p1 and p2."""
    x1,y1=p1
    x2,y2=p2
    return math.sqrt((x1-x2)**2+(y1-y2)**2)

def findClosestPoint(p,pts):
    """Find the closest points to p in pts."""
    npts=[(distance(p,pts[i]),i) for i in range(len(pts))]
    return sorted(npts)[0][1]


def naivePathFinding(points,i=0):
    """Find a path by finding for each point the next closest one.
    i is the start index."""
    path=[]
    while len(points)>0:
        points=points[i]
        del points[i]
        i=findClosestPoint(points[i])
        path.append(point)
    return path



if __name__=="__main__":
    #x,y=points[0]
    #p=set(points)
    #e=Entity(x,y,0)
    #print(len(points))
    #d=makeDictionary(points)
    #gs,pts=solvePoints(points)
    points=list(set(points))
    naivePathFinding(points)

    #print(len(pts))
    #print(len(gs))
