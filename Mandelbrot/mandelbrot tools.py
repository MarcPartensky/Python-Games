#from mycontext import Context
from PIL import Image, ImageDraw
import numpy as np
import colors

def getDiscreteColoredArray(array,color1=colors.WHITE,color2=colors.BLACK):
    f=lambda n:color1 if n==1 else color2
    return f(array)


def uselessNameSpace():
    for y in range(HAUTEUR):
      for x in range(LARGEUR):
        # Les deux lignes suivantes permettent d'associer à chaque pixel de l'écran de coordonnées (x;y)
        # un point C du plan de coordonnées (cx;cy) dans le repère défini par XMIN:XMAX et YMIN:YMAX
        cx = (x * (XMAX - XMIN) / LARGEUR + XMIN)
        cy = (y * (YMIN - YMAX) / HAUTEUR + YMAX)
        xn = 0
        yn = 0
        n = 0
        while (xn * xn + yn * yn) < 4 and n < MAX_ITERATION: # on teste que le carré de la distance est inférieur à 4 -> permet d'économiser un calcul de racine carrée coûteux en terme de performances
          # Calcul des coordonnes de Mn
          tmp_x = xn
          tmp_y = yn
          xn = tmp_x * tmp_x - tmp_y * tmp_y + cx
          yn = 2 * tmp_x * tmp_y + cy



def showMatrixWithScreen(screen,array,width=None,height=None):
    if not width or not height:
        width,height=[len(array),len(array[0])]
    for x in range(width):
        for y in range(height):
            screen.set_at((x, y),array[x][y])

def showMatrixWithContext(context,array,width=None,height=None):
    if not width or not height:
        width,height=[len(array),len(array[0])]
    for x in range(width):
        for y in range(height):
            context.draw.square()








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


if __name__=="__main__":
    #context=Context()
    #width,height=context.size
    width=800;height=600;maxiter=20
    matrix=getMatrix(width,height,maxiter=maxiter)
    showMatrixWithPIL(matrix,width,height,maxiter=maxiter)
