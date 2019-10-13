from mycontext import Context
from PIL import Image, ImageDraw
import numpy as np
import mycolors
from mymanager import SimpleManager



def mandelbrot(z,maxiter):
    c=z
    for n in range(maxiter):
        if abs(z) > 2:
            return n
        z=z**2+c
    return maxiter

def getMatrix(width=800,height=800,corners=[-2,-1,1,1],maxiter=80):
    xmin,ymin,xmax,ymax=corners
    xzoom=(xmax-xmin)/width
    yzoom=(ymax-ymin)/height
    matrix=np.zeros([width,height])
    for x in range(0,width):
        for y in range(0,height):
            matrix[x][y]=mandelbrot(complex(xmin+x*xzoom,ymin+y*yzoom),maxiter)
    return matrix

def showMatrixWithPIL(matrix,width=None,height=None,maxiter=80,save=True):
    if (width is None) or (height is None):
        width,height=[len(matrix),len(matrix[0])]
    im = Image.new('RGB',(width,height),(0, 0, 0))
    draw = ImageDraw.Draw(im)
    for x in range(width):
        for y in range(height):
            color=int(matrix[x][y] * 255 / maxiter)
            draw.point([x, y], (color, color, color))
    if save: im.save('output.png', 'PNG')
    im.show()



class Mandelbrot(SimpleManager):
    def compute(self,z):
        c=z
        for n in range(self.maxiter):
            if abs(z) > 2:
                return n
            z=z**2+c
        return self.maxiter

    def __init__(self,context,size,maxiter=80):
        """Create a set of mandelbrot using the size, the corners and the maxiter (maxiteration)."""
        self.context=context
        self.maxiter=maxiter
        self.size=size

    def buildMatrix(self):
        """Return the numpy matrix of the set."""
        xmin,ymin,xmax,ymax=self.corners
        xzoom=(xmax-xmin)/self.width
        yzoom=(ymax-ymin)/self.height
        self.matrix=np.zeros(self.size)
        for x in range(self.width):
            for y in range(self.height):
                self.matrix[x][y]=self.compute(complex(xmin+x*xzoom,ymin+y*yzoom))

    def showWithPIL(self,save=True):
        """Show the set with PIL using the matrix."""
        im = Image.new('RGB',(self.width,self.height),(0, 0, 0))
        draw = ImageDraw.Draw(im)
        for x in range(self.width):
            for y in range(self.height):
                color=int(self.matrix[x][y] * 255 / self.maxiter)
                draw.point([x, y], (color, color, color))
        if save: im.save('output.png', 'PNG')
        im.show()

    def showSet(self):
        """Show the mandelbrot set on the context."""
        for x in range(self.width):
            for y in range(self.height):
                c=int(self.matrix[x][y] * 255 / self.maxiter)
                self.context.draw.rect(self.context.screen,(c,c,c),[x,y,1,1])


    def update(self):
        """Update the mandelbrot set depending on the corners."""
        self.buildMatrix()

    def show(self):
        """Show the mandelbrot set."""
        self.context.refresh()
        self.context.control()
        self.showSet()
        self.context.flip()

    def getCorners(self):
        return self.context.corners
    def getWidth(self):
        return self.size[0]
    def getHeight(self):
        return self.size[1]

    #Properties
    corners=property(getCorners)
    height=property(getHeight)
    width=property(getWidth)



if __name__=="__main__":
    context_size=[800,600]
    mandelbrot_size=[200,150]
    corners=[-2,-1,1,1]
    context=Context.createFromSizeAndCorners(context_size,corners,name="Mandelbrot")    #width,height=context.size

    print(context.corners)
    print(context.position)
    print([0,0] in context)
    #width=800;height=600;maxiter=20
    #matrix=getMatrix(width,height,maxiter=maxiter)
    #showMatrixWithPIL(matrix,width,height,maxiter=maxiter)
    m=Mandelbrot(context,mandelbrot_size)
    m()
