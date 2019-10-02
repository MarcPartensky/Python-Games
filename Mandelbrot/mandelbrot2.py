from PIL import Image, ImageDraw
import numpy as np
#from mandelbrot import mandelbrot, MAX_ITER

MAX_ITER = 80

def mandelbrot(c,maxiter):
    z = 0
    n = 0
    while abs(z) <= 2 and n < maxiter:
        z = z**2 + c
        n += 1
    return n

# Image size (pixels)


def showPicture(corners=[-2,-1,1,1],width=600,height=400,maxiter=80):
    xmin,ymin,xmax,ymax=corners

    im = Image.new('RGB', (width,height), (0, 0, 0))
    draw = ImageDraw.Draw(im)
    xlength=xmax-xmin
    ylenght=ymax-ymin

    #from pixel to complex
    xzoom=xlength/width
    yzoom=ylenght/height

    for x in range(width):
        for y in range(height):
            # Convert pixel coordinate to complex number
            c = complex(xmin+x*xzoom,ymin+y*yzoom)
            # Compute the number of iterations
            m = mandelbrot(c,maxiter)
            # The color depends on the number of iterations
            color = int(m * 255 / maxiter)
            # Plot the point
            draw.point([x, y], (color, color, color))

    im.save('output.png', 'PNG')
    im.show()

def getMatrix(corners=[-2,-1,1,1],width=600,height=400,maxiter=80):
    xmin,ymin,xmax,ymax=corners
    xzoom=(xmax-xmin)/width
    yzoom=ymax-ymin/height
    matrix=np.zeros([width,height])
    for x in range(0,width):
        for y in range(0,height):
            c = complex(xmin+x*xzoom,ymin+y*yzoom)
            m = mandelbrot(c,maxiter)
            matrix[x,y]=m
    return matrix

#matrix=getMatrix()
#print(len(matrix))
showPicture()
