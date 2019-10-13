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

    def __init__(self,context,precisions,maxiter=80):
        """Create a set of mandelbrot using the size, the corners and the maxiter (maxiteration)."""
        self.context=context
        self.maxiter=maxiter
        self.precisions=precisions
        self.n=0

    def buildMatrix(self):
        """Build the matrix."""
        xmin,ymin,xmax,ymax=self.corners
        sx,sy=self.size
        dx=xmax-xmin; dy=ymax-ymin
        self.matrix=np.zeros(self.size)
        for ix in range(sx):
            for iy in range(sy):
                x=xmin+dx*ix/sx
                y=ymin+dy*iy/sy
                z=complex(x,y)
                self.matrix[ix][iy]=self.compute(z)

    def oldbuildMatrix(self):
        """Return the numpy matrix of the set."""
        xmin,ymin,xmax,ymax=self.corners
        xzoom=(xmax-xmin)/self.width
        yzoom=(ymax-ymin)/self.height
        print(self.size)
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
        xmin,ymin,xmax,ymax=self.corners
        sx,sy=self.size
        dx,dy=xmax-xmin,ymax-ymin
        csx,csy=self.context.size
        qsx,qsy=csx/sx,csy/sy
        cmax=np.max(self.matrix)
        cmin=np.min(self.matrix)
        dc=cmax-cmin
        for ix in range(self.width):
            for iy in range(self.height):
                c=int(255*(self.matrix[ix][iy]-cmin)/dc) #color
                x,y=csx*ix/sx,csy-csy*iy/sy
                self.context.draw.window.draw.rect(self.context.screen,(c,c,c),[x,y,qsx,qsy])

    def update(self):
        """Update the mandelbrot set depending on the corners."""
        self.buildMatrix()

    def show(self):
        """Show the mandelbrot set."""
        self.context.refresh()
        self.context.control()
        self.showSet()
        self.context.flip()

    def reactKeyDown(self,key):
        """React to a keydown event."""
        if key == K_ESCAPE:
            self.context.open=False


    #Properties
    def getCorners(self):
        return self.context.corners
    def getWidth(self):
        return self.context.width//self.precisions[self.n]
    def getHeight(self):
        return self.context.height//self.precisions[self.n]
    def getSize(self):
        return [c//self.precisions[self.n] for c in self.context.size]

    #Properties
    corners=property(getCorners)
    height=property(getHeight)
    width=property(getWidth)
    size=property(getSize)



if __name__=="__main__":
    context_size=[800,600]
    precisions=[10,5,2,1]
    maxiter=80
    corners=[-2,-1,1,1]
    context=Context.createFromSizeAndCorners(context_size,corners,name="Mandelbrot")    #width,height=context.size
    m=Mandelbrot(context,precisions,maxiter)
    m()
