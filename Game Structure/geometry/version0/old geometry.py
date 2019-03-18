from mycolors import WHITE
from mymaths import mean,pi
from mywindow import Window


class Trace:
    def __init__(self,color=WHITE):
        self.color=color


class Form(Trace):
    def __init__(self,points,color=WHITE):
        Trace.__init__(self,color)
        self.points=points
        self.center=self.center(self.points)
    def center(self,points):
        mx=mean([point.x for point in points])
        my=mean([point.y for point in points])
        return [mx,my]
    def rotate(self,center=None,angle=pi):
        if center==None:
            center=self.center(self.points)
    def __getitem__(self, index):
        return self.points[index]
    def __setitem__(self, index, value):
        self.points[index]=value



class Circle(Trace):
    def __init__(self,*args,radius=10,color=WHITE):
        Trace.__init__(self,color)
        #self.x=x
        #self.y=y
        self.position=list(args)
        self.radius=radius
        self.color=color
    def show(self,window):
        pass


class Point(Circle):
    def __init__(self,x,y,radius=1,color=WHITE):
        Circle.__init__(self,x,y,radius=radius,color=color)
    def __getitem__(self, index):
        return self.position[index]
    def __setitem__(self, index, value):
        self.position[index]=value

class Line(Form):
    def __init__(self,p1,p2,color=WHITE):
        Form.__init__(self,[p1,p2],color)
        if p1.x!=p2.x:
            self.a=(p2.y-p1.y)/(p2.x-p1.x)
        else:
            self.a=None
        if self.a!=None:
            self.b=p1.y-self.a*p1.x
        else:
            self.b=None
    def show(self,window):
        pass


class Segment(Line):
    def __init__(self,p1,p2,color=WHITE):
        Line.__init__(self,p1,p2)
        self.p1=p1
        self.p2=p2

    def __mul__(self,other):
        Mx=max(self.p1[0],self.p2[1])
        My
        return True

    def show(self,window):
        window.draw.line(window.screen,self.color,[p1[0],p1[1]],[p2[0],p2[1]],1)

    def showAll(self,window):
        pass




class Polygone(Form):
    def __init__(self,points):
        self.points=points
        self.segments=[Segment(points[i%len(points)],points[(i+1)%len(points)]) for i in range(len(points))]
    def __mul__(self,other):
        pass


class Triangle(Polygone):
    def __init__(self,points):
        Polygone.__init__(points)


class Square(Polygone):
    def __init__(self,points):
        Polygone.__init__(points)

"""
Syntax:
segment1*segment2=>bool
polygone1*polygone2=>bool

x:p.position[0]
x:p.x
x:p[0]
"""



if __name__=="__main__":
    window=Window()
    p1=Point(15,200)
    p2=Point(540,54)
    #s=Segment(p1,p2)
    print(p1.x)
    s.show(window)
    window()
