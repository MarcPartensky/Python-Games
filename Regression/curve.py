import pygame
import random

def prd(list):
    result=1
    for e in list:
        result*=e
    return result

class Curve:
    def __init__(self,points,degree=2):
        #print(points)
        self.points=points
        self.degree=degree
        self.coefficients=[0 for i in range(self.degree+1)]
        self.cout=10**10

    def evaluate(self,x,coefficients):
        y=0
        for n,coefficient in enumerate(coefficients):
            y+=coefficient*x**n
            #print(n,coefficient)
            #print(x,)
        return y

    def cost(self,coefficients):
        s=0
        for A in self.points:
            x,y=A
            z=self.evaluate(x,coefficients)
            s+=(z-y)**2
        #print(s)
        return s

    def adjust(self):
        xs=1  #x step
        ys=1  #y step
        epochs=100 #epochs
        #precision=2
        #delta=1
        #epsilon=10**(-precision)
        for e in range(epochs):
            p=100/(e+1)
            costs=[]
            #x,y=self.coefficients
            #tests=[(x+p*i,y+p*j) for j in range(-1,2) for i in range(-1,2)]
            tests=[]
            for coefficient in self.coefficients:
                for i in range(-1,2):
                    #tests=[(x+p*i,y+p*j) for j in range(-1,2) for i in range(-1,2)]
                    tests.append(coefficient+p*i)

            #tests=[]
            #for test in old_tests:
            #tests.append(test)
            for test in tests:
                costs.append(self.cost(test))
            #print(tests)
            #print(costs)
            #print(min(costs))
            self.coefficients=tests[costs.index(min(costs))]
            #print(self.coefficients)

    def squareAdjust(self,precision=100):
        costs,tests=[],[]
        for y in range(-precision,precision):
            for x in range(-precision,precision):
                test=(7*x,6*y)
                #print(test)
                costs.append(self.cost(test))
                tests.append(test)
        #print(min(costs))
        self.coefficients=tests[costs.index(min(costs))]

    def linearRegression(self,points):
        X=[point[0] for point in points]
        Y=[point[1] for point in points]
        x_=sum(X)/len(points)
        y_=sum(Y)/len(points)
        #print([(x-x_)*(y-y_) for x,y in zip(X,Y)])
        a=sum([(x-x_)*(y-y_) for x,y in zip(X,Y)])/sum([(x-x_)**2 for x,y in zip(X,Y)])
        b=y_-a*x_
        print(a,b)
        self.coefficients=[b,a]

    def polynomialRegression(self,x,points):
        points=list(set(points))
        X=[p[0] for p in points]
        Y=[p[1] for p in points]
        #print(X,Y)
        n=len(points)
        return sum([Y[j]*prd([(x-X[i])/(X[i]-X[j]) for i in range(n) if i!=j]) for j in range(n)])



    def show(self,window):
        self.showPoints(window)
        self.showCurve(window)

    def showPoints(self,window,radius=5):
        color=window.randomColor()
        for point in self.points:
            pygame.draw.circle(window.screen,color,point,radius,0)

    def showLine(self,window):
        color=window.reverseColor(window.background_color)
        precision=1
        sx,sy=window.size
        points=[]
        for x in range(sx):
            points.append((x,self.evaluate(x,self.coefficients)))
        pygame.draw.lines(window.screen, color, False, points, 1)

    def showCurve(self,window):
        color=window.reverseColor(window.background_color)
        precision=1
        sx,sy=window.size
        points=[]
        for x in range(sx):
            points.append((x,self.polynomialRegression(x,self.points)))
        #print(points)
        pygame.draw.lines(window.screen, color, False, points, 1)



        """
        for x in range(1,sx,precision):
            end=(x,self.evaluate(x))
            print(start,end)
            pygame.draw.lines(window.screen,color,start,end,0)
            start=end
        """
